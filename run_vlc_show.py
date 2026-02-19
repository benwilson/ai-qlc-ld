#!/usr/bin/env python3
import argparse
import os
import signal
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from threading import Event, Thread
from typing import Dict, Optional, Tuple

from qlc_runtime.artnet import ARTNET_PORT, ArtNetSender
from qlc_runtime.engine import (
    COMPLETED,
    STOPPED,
    TIMEOUT,
    make_blackout_frame,
    run_function,
)
from qlc_runtime.model import ChaserFunction, SceneFunction
from qlc_runtime.network import LIMITED_BROADCAST, derive_broadcast_ip
from qlc_runtime.parser import parse_workspace
from qlc_runtime.select import select_target_function
from qlc_runtime.show_match import index_shows, match_show_for_media
from qlc_runtime.vlc_http import DEFAULT_VLC_URL, extract_media_basename, get_vlc_status

TRUE_VALUES = {"1", "true", "yes", "on", "y", "t"}
FALSE_VALUES = {"0", "false", "no", "off", "n", "f"}


def send_blackout(sender, repeats: int = 3, interval_s: float = 0.03) -> None:
    blackout = make_blackout_frame()
    for _ in range(max(1, repeats)):
        try:
            sender.send(blackout)
        except OSError:
            break
        time.sleep(max(0.0, interval_s))


@dataclass(frozen=True)
class ResolvedRun:
    status_state: str
    media_name: str
    show_path: Path
    workspace: object
    function_id: int
    selected_from: str
    function: object
    bind_ip: Optional[str]
    target_ip: str
    target_universe: int
    auto_target: bool
    auto_target_source: Optional[str]
    start_offset_ms: int

    @property
    def identity(self) -> Tuple[str, int, str, int, str]:
        return (
            str(self.show_path),
            int(self.function_id),
            str(self.target_ip),
            int(self.target_universe),
            str(self.bind_ip or ""),
        )


class ActiveRun:
    def __init__(self, resolved: ResolvedRun, args):
        self.resolved = resolved
        self.args = args
        self.stop_event = Event()
        self.sender = ArtNetSender(
            ip=resolved.target_ip,
            universe=resolved.target_universe,
            port=args.port,
            dry_run=args.dry_run,
            bind_ip=resolved.bind_ip,
        )
        self.started_at = time.monotonic()
        self.start_offset_ms = resolved.start_offset_ms
        self.result = None
        self.error: Optional[BaseException] = None
        self._closed = False
        self.thread = Thread(target=self._run, daemon=True, name="vlc-show-runner")
        self.thread.start()

    @property
    def identity(self) -> Tuple[str, int, str, int, str]:
        return self.resolved.identity

    def _run(self) -> None:
        try:
            def on_step(step_index: int, fade_ms: int, hold_ms: int, step_count: int, scene_name: str):
                print(
                    f"Step: idx={step_index} scene={scene_name!r} "
                    f"fade={fade_ms}ms hold={hold_ms}ms"
                )

            callback = on_step if (self.args.verbose or isinstance(self.resolved.function, ChaserFunction)) else None
            self.result = run_function(
                workspace=self.resolved.workspace,
                function_id=self.resolved.function_id,
                universe=self.resolved.target_universe,
                sender=self.sender,
                fps=self.args.fps,
                max_seconds=None,
                should_stop=self.stop_event.is_set,
                on_step=callback,
                start_offset_ms=self.resolved.start_offset_ms,
            )
        except BaseException as exc:  # pragma: no cover - safety net for runner thread
            self.error = exc

    def is_done(self) -> bool:
        return not self.thread.is_alive()

    def expected_offset_ms(self) -> int:
        elapsed_ms = int((time.monotonic() - self.started_at) * 1000.0)
        return self.start_offset_ms + max(0, elapsed_ms)

    def shutdown(self, blackout: bool = False) -> None:
        if self._closed:
            return
        self.stop_event.set()
        self.thread.join(timeout=2.0)
        if blackout:
            send_blackout(self.sender)
        self.sender.close()
        self._closed = True


def _parse_env_file(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    env_path = Path(path)
    if not env_path.exists() or not env_path.is_file():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        value = raw_value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values


def _lookup_env_value(
    env_keys,
    dotenv_values: Dict[str, str],
):
    for key in env_keys:
        shell_value = os.getenv(key)
        if shell_value is not None:
            return shell_value
        if key in dotenv_values:
            return dotenv_values[key]
    return None


def _coerce_string(name: str, value) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _coerce_int(name: str, value) -> Optional[int]:
    text = _coerce_string(name, value)
    if text is None:
        return None
    try:
        return int(text)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid {name} value {value!r}; expected integer") from exc


def _coerce_float(name: str, value) -> Optional[float]:
    text = _coerce_string(name, value)
    if text is None:
        return None
    try:
        return float(text)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid {name} value {value!r}; expected number") from exc


def _coerce_bool(name: str, value) -> Optional[bool]:
    text = _coerce_string(name, value)
    if text is None:
        return None
    if isinstance(value, bool):
        return value
    text = text.casefold()
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES:
        return False
    raise ValueError(
        f"Invalid {name} value {value!r}; expected one of "
        f"{sorted(TRUE_VALUES | FALSE_VALUES)}"
    )


def _resolve_value(
    name: str,
    cli_value,
    env_keys,
    dotenv_values: Dict[str, str],
    default_value,
    coerce,
):
    if cli_value is not None:
        return coerce(name, cli_value)
    raw = _lookup_env_value(env_keys, dotenv_values)
    if raw is None:
        return default_value
    coerced = coerce(name, raw)
    if coerced is None:
        return default_value
    return coerced


def _apply_env_defaults(args, env_file_from_cli: bool = False) -> None:
    dotenv_values = _parse_env_file(Path(args.env_file))
    if not env_file_from_cli:
        env_file_override = _lookup_env_value(["RUN_VLC_SHOW_ENV_FILE"], dotenv_values)
        env_file_override = _coerce_string("env_file", env_file_override)
        if env_file_override and env_file_override != args.env_file:
            args.env_file = env_file_override
            dotenv_values = _parse_env_file(Path(args.env_file))

    args.shows_dir = _resolve_value(
        "shows_dir",
        args.shows_dir,
        ["RUN_VLC_SHOW_SHOWS_DIR"],
        dotenv_values,
        None,
        _coerce_string,
    )

    args.ip = _resolve_value("ip", args.ip, ["RUN_VLC_SHOW_IP"], dotenv_values, None, _coerce_string)
    args.bind_ip = _resolve_value(
        "bind_ip",
        args.bind_ip,
        ["RUN_VLC_SHOW_BIND_IP"],
        dotenv_values,
        None,
        _coerce_string,
    )
    args.universe = _resolve_value(
        "universe",
        args.universe,
        ["RUN_VLC_SHOW_UNIVERSE"],
        dotenv_values,
        None,
        _coerce_int,
    )
    args.port = _resolve_value("port", args.port, ["RUN_VLC_SHOW_PORT"], dotenv_values, ARTNET_PORT, _coerce_int)

    args.button_id = _resolve_value(
        "button_id",
        args.button_id,
        ["RUN_VLC_SHOW_BUTTON_ID"],
        dotenv_values,
        None,
        _coerce_int,
    )
    args.button_caption = _resolve_value(
        "button_caption",
        args.button_caption,
        ["RUN_VLC_SHOW_BUTTON_CAPTION"],
        dotenv_values,
        None,
        _coerce_string,
    )
    args.function_id = _resolve_value(
        "function_id",
        args.function_id,
        ["RUN_VLC_SHOW_FUNCTION_ID"],
        dotenv_values,
        None,
        _coerce_int,
    )

    args.fps = _resolve_value("fps", args.fps, ["RUN_VLC_SHOW_FPS"], dotenv_values, 40, _coerce_int)
    args.max_seconds = _resolve_value(
        "max_seconds",
        args.max_seconds,
        ["RUN_VLC_SHOW_MAX_SECONDS"],
        dotenv_values,
        None,
        _coerce_float,
    )
    args.dry_run = _resolve_value(
        "dry_run",
        args.dry_run,
        ["RUN_VLC_SHOW_DRY_RUN"],
        dotenv_values,
        False,
        _coerce_bool,
    )
    args.verbose = _resolve_value(
        "verbose",
        args.verbose,
        ["RUN_VLC_SHOW_VERBOSE"],
        dotenv_values,
        False,
        _coerce_bool,
    )

    args.vlc_url = _resolve_value(
        "vlc_url",
        args.vlc_url,
        ["RUN_VLC_SHOW_VLC_URL", "VLC_HTTP_URL"],
        dotenv_values,
        DEFAULT_VLC_URL,
        _coerce_string,
    )
    args.vlc_password = _resolve_value(
        "vlc_password",
        args.vlc_password,
        ["RUN_VLC_SHOW_VLC_PASSWORD", "VLC_HTTP_PASSWORD"],
        dotenv_values,
        None,
        _coerce_string,
    )
    args.vlc_timeout = _resolve_value(
        "vlc_timeout",
        args.vlc_timeout,
        ["RUN_VLC_SHOW_VLC_TIMEOUT", "VLC_HTTP_TIMEOUT"],
        dotenv_values,
        1.0,
        _coerce_float,
    )

    args.follow = _resolve_value(
        "follow",
        args.follow,
        ["RUN_VLC_SHOW_FOLLOW"],
        dotenv_values,
        False,
        _coerce_bool,
    )
    args.poll_interval = _resolve_value(
        "poll_interval",
        args.poll_interval,
        ["RUN_VLC_SHOW_POLL_INTERVAL"],
        dotenv_values,
        0.5,
        _coerce_float,
    )
    args.resync_threshold = _resolve_value(
        "resync_threshold",
        args.resync_threshold,
        ["RUN_VLC_SHOW_RESYNC_THRESHOLD"],
        dotenv_values,
        1.0,
        _coerce_float,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sync ArtNet show playback to VLC current track/time"
    )
    parser.add_argument(
        "shows_dir",
        nargs="?",
        default=None,
        help="Directory containing .qxw show files (recursive exact stem match)",
    )

    parser.add_argument("--ip", default=None, help="Override ArtNet target IP from .qxw")
    parser.add_argument(
        "--bind-ip",
        default=None,
        help="Bind UDP socket to a specific local interface IP (optional)",
    )
    parser.add_argument("--universe", type=int, default=None, help="Override universe ID")
    parser.add_argument("--port", type=int, default=None, help="ArtNet UDP port")

    parser.add_argument("--button-id", type=int, default=None, help="Select VC button by ID")
    parser.add_argument(
        "--button-caption",
        default=None,
        help="Select VC button by caption (case-insensitive exact match)",
    )
    parser.add_argument("--function-id", type=int, default=None, help="Run function ID directly")

    parser.add_argument("--fps", type=int, default=None, help="Frame rate for fade interpolation")
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=None,
        help="Runtime limit (one-shot: runner limit, follow: supervisor limit)",
    )
    parser.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Parse/schedule only; no UDP send",
    )
    parser.add_argument(
        "--verbose",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Verbose runtime logs",
    )

    parser.add_argument("--env-file", default=None, help="Path to .env config file")
    parser.add_argument("--vlc-url", default=None, help="VLC HTTP base URL")
    parser.add_argument(
        "--vlc-password",
        default=None,
        help=(
            "VLC HTTP password (default: RUN_VLC_SHOW_VLC_PASSWORD "
            "or legacy VLC_HTTP_PASSWORD from env/.env)"
        ),
    )
    parser.add_argument("--vlc-timeout", type=float, default=None, help="VLC HTTP timeout in seconds")

    parser.add_argument(
        "--follow",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Continuously follow VLC state",
    )
    parser.add_argument("--poll-interval", type=float, default=None, help="Follow mode poll interval")
    parser.add_argument(
        "--resync-threshold",
        type=float,
        default=None,
        help="Restart run when drift from VLC exceeds this many seconds",
    )

    return parser


def _resolve_target(workspace, args) -> Tuple[Optional[str], str, int, bool, Optional[str]]:
    bind_ip = args.bind_ip or workspace.artnet_ip
    target_ip = args.ip
    auto_target = False
    auto_target_source = None

    if target_ip is None:
        if bind_ip:
            target_ip, auto_target_source = derive_broadcast_ip(bind_ip)
            auto_target = True
        elif args.dry_run:
            target_ip = "0.0.0.0"
        else:
            raise ValueError("No ArtNet target IP found. Pass --ip (node or broadcast IP).")

    target_universe = args.universe
    if target_universe is None:
        target_universe = workspace.artnet_universe if workspace.artnet_universe is not None else 0

    return bind_ip, target_ip, int(target_universe), auto_target, auto_target_source


def _resolve_run_for_status(args, show_index, status) -> ResolvedRun:
    media_name = extract_media_basename(status)
    if not media_name:
        raise ValueError("VLC status did not include a playable media name")

    show_path = match_show_for_media(media_name, show_index)
    workspace = parse_workspace(str(show_path))
    function_id, selected_from = select_target_function(
        workspace,
        function_id=args.function_id,
        button_id=args.button_id,
        button_caption=args.button_caption,
    )
    function = workspace.functions[function_id]
    if not isinstance(function, (SceneFunction, ChaserFunction)):
        raise ValueError(
            f"Unsupported target function type {type(function).__name__} (ID {function_id})"
        )

    bind_ip, target_ip, target_universe, auto_target, auto_target_source = _resolve_target(
        workspace,
        args,
    )
    offset_ms = int(max(0.0, float(status.time_s)) * 1000.0)

    return ResolvedRun(
        status_state=status.state,
        media_name=media_name,
        show_path=show_path,
        workspace=workspace,
        function_id=function_id,
        selected_from=selected_from,
        function=function,
        bind_ip=bind_ip,
        target_ip=target_ip,
        target_universe=target_universe,
        auto_target=auto_target,
        auto_target_source=auto_target_source,
        start_offset_ms=offset_ms,
    )


def _print_run_header(resolved: ResolvedRun, args) -> None:
    print(
        f"VLC: state={resolved.status_state or 'unknown'} "
        f"media={resolved.media_name!r} time={resolved.start_offset_ms / 1000.0:.3f}s"
    )
    print(f"Show: {resolved.show_path}")
    print(f"Selected: {resolved.selected_from}")
    print(
        f"Function: ID={resolved.function_id} Name={resolved.function.name!r} "
        f"Type={type(resolved.function).__name__}"
    )
    print(
        f"ArtNet: {resolved.target_ip}:{args.port} universe={resolved.target_universe} "
        f"mode={'dry-run' if args.dry_run else 'live'} fps={args.fps}"
    )
    print(f"Bind IP: {resolved.bind_ip or 'auto'}")
    if resolved.auto_target:
        source = resolved.auto_target_source or "auto"
        if resolved.target_ip == LIMITED_BROADCAST:
            print(
                f"Target auto-selected from bind/workspace IP {resolved.bind_ip} -> "
                f"{resolved.target_ip} ({source})"
            )
            print(
                "Warning: using limited broadcast fallback. "
                "If fixtures do not respond, pass --ip with your directed broadcast.",
                file=sys.stderr,
            )
        else:
            print(
                f"Target auto-selected from bind/workspace IP {resolved.bind_ip} -> "
                f"{resolved.target_ip} ({source})"
            )
    if not args.dry_run and resolved.bind_ip and resolved.target_ip == resolved.bind_ip:
        print(
            "Warning: target IP equals bind/local IP; this usually means sending to self.",
            file=sys.stderr,
        )


def _fetch_status_or_raise(args):
    password = args.vlc_password
    if isinstance(password, str) and password == "":
        password = None
    return get_vlc_status(
        base_url=args.vlc_url,
        password=password,
        timeout_s=max(0.1, float(args.vlc_timeout)),
    )


def _run_once(args, show_index) -> int:
    try:
        status = _fetch_status_or_raise(args)
    except Exception as exc:
        print(f"Error: VLC status request failed: {exc}", file=sys.stderr)
        return 2

    if status.state not in {"playing", "paused"}:
        print(
            f"Error: VLC is not playing media (state={status.state!r})",
            file=sys.stderr,
        )
        return 2

    try:
        resolved = _resolve_run_for_status(args, show_index, status)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    _print_run_header(resolved, args)

    if args.max_seconds is not None:
        print(f"Max runtime: {args.max_seconds:.2f}s")

    stop_event = Event()
    signal_name = {"name": None}

    def _handle_signal(signum, _frame):
        signal_name["name"] = signal.Signals(signum).name
        stop_event.set()

    sender = ArtNetSender(
        ip=resolved.target_ip,
        universe=resolved.target_universe,
        port=args.port,
        dry_run=args.dry_run,
        bind_ip=resolved.bind_ip,
    )
    try:
        try:
            signal.signal(signal.SIGINT, _handle_signal)
            signal.signal(signal.SIGTERM, _handle_signal)
        except ValueError:
            pass

        def on_step(step_index: int, fade_ms: int, hold_ms: int, step_count: int, scene_name: str):
            print(
                f"Step: idx={step_index} scene={scene_name!r} "
                f"fade={fade_ms}ms hold={hold_ms}ms"
            )

        callback = on_step if (args.verbose or isinstance(resolved.function, ChaserFunction)) else None

        try:
            result = run_function(
                workspace=resolved.workspace,
                function_id=resolved.function_id,
                universe=resolved.target_universe,
                sender=sender,
                fps=args.fps,
                max_seconds=args.max_seconds,
                should_stop=stop_event.is_set,
                on_step=callback,
                start_offset_ms=resolved.start_offset_ms,
            )
        except OSError as exc:
            print(
                f"Error: ArtNet send failed: {exc}. "
                "Try --bind-ip <local-nic-ip> and/or explicit --ip <node-or-broadcast-ip>.",
                file=sys.stderr,
            )
            return 2

        stop_reason = result.reason
        if stop_reason == STOPPED and signal_name["name"]:
            stop_reason = f"signal {signal_name['name']}"
        elif stop_reason == TIMEOUT:
            stop_reason = "timeout"
        elif stop_reason == COMPLETED:
            stop_reason = "completed"
        print(f"Stop reason: {stop_reason}")
        return 0
    finally:
        send_blackout(sender)
        sender.close()


def _run_follow(args, show_index) -> int:
    if args.poll_interval <= 0:
        print("Error: --poll-interval must be > 0", file=sys.stderr)
        return 2
    if args.resync_threshold < 0:
        print("Error: --resync-threshold must be >= 0", file=sys.stderr)
        return 2

    stop_event = Event()
    signal_name = {"name": None}

    def _handle_signal(signum, _frame):
        signal_name["name"] = signal.Signals(signum).name
        stop_event.set()

    try:
        signal.signal(signal.SIGINT, _handle_signal)
        signal.signal(signal.SIGTERM, _handle_signal)
    except ValueError:
        pass

    active: Optional[ActiveRun] = None
    started_supervisor = time.monotonic()

    def _shutdown_active(blackout: bool) -> None:
        nonlocal active
        if active is None:
            return
        active.shutdown(blackout=blackout)
        active = None

    while not stop_event.is_set():
        if args.max_seconds is not None and (time.monotonic() - started_supervisor) >= args.max_seconds:
            break

        if active is not None and active.is_done():
            done = active
            _shutdown_active(blackout=False)
            if done.error is not None:
                print(f"Runner error: {done.error}", file=sys.stderr)
            elif done.result is not None:
                print(f"Runner stop reason: {done.result.reason}")

        try:
            status = _fetch_status_or_raise(args)
        except Exception as exc:
            print(f"Warning: VLC status request failed: {exc}", file=sys.stderr)
            time.sleep(args.poll_interval)
            continue

        media_name = extract_media_basename(status)
        if status.state == "paused":
            if active is not None:
                print("VLC paused; stopping active run.")
                _shutdown_active(blackout=False)
            time.sleep(args.poll_interval)
            continue

        if status.state != "playing" or not media_name:
            if active is not None:
                print("VLC has no active track; stopping active run.")
                _shutdown_active(blackout=True)
            time.sleep(args.poll_interval)
            continue

        try:
            resolved = _resolve_run_for_status(args, show_index, status)
        except Exception as exc:
            print(f"Warning: cannot resolve show for VLC track: {exc}", file=sys.stderr)
            if active is not None:
                _shutdown_active(blackout=True)
            time.sleep(args.poll_interval)
            continue

        if active is None:
            _print_run_header(resolved, args)
            print("Follow: starting synced run")
            active = ActiveRun(resolved, args)
            time.sleep(args.poll_interval)
            continue

        if active.identity != resolved.identity:
            print("Follow: track/function changed; restarting run")
            _shutdown_active(blackout=False)
            _print_run_header(resolved, args)
            active = ActiveRun(resolved, args)
            time.sleep(args.poll_interval)
            continue

        drift_ms = abs(active.expected_offset_ms() - resolved.start_offset_ms)
        if drift_ms > int(args.resync_threshold * 1000.0):
            print(
                f"Follow: drift {drift_ms}ms exceeds threshold "
                f"{int(args.resync_threshold * 1000.0)}ms; resyncing"
            )
            _shutdown_active(blackout=False)
            _print_run_header(resolved, args)
            active = ActiveRun(resolved, args)

        time.sleep(args.poll_interval)

    if signal_name["name"]:
        print(f"Stop reason: signal {signal_name['name']}")
    elif args.max_seconds is not None:
        print("Stop reason: timeout")
    else:
        print("Stop reason: stopped")

    _shutdown_active(blackout=True)
    return 0


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    env_file_from_cli = args.env_file is not None
    args.env_file = args.env_file or os.getenv("RUN_VLC_SHOW_ENV_FILE") or ".env"
    try:
        _apply_env_defaults(args, env_file_from_cli=env_file_from_cli)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if not args.shows_dir:
        print(
            "Error: shows_dir is required (pass positional shows_dir or set RUN_VLC_SHOW_SHOWS_DIR).",
            file=sys.stderr,
        )
        return 2

    shows_dir = Path(args.shows_dir)
    try:
        show_index = index_shows(shows_dir)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    if not show_index:
        print(f"Error: no .qxw files found under {shows_dir}", file=sys.stderr)
        return 2

    if args.follow:
        return _run_follow(args, show_index)
    return _run_once(args, show_index)


if __name__ == "__main__":
    raise SystemExit(main())
