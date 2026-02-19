#!/usr/bin/env python3
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from run_vlc_show import _apply_env_defaults, _parse_env_file


def _blank_args(env_file: str) -> Namespace:
    return Namespace(
        shows_dir=None,
        ip=None,
        bind_ip=None,
        universe=None,
        port=None,
        button_id=None,
        button_caption=None,
        function_id=None,
        fps=None,
        max_seconds=None,
        dry_run=None,
        verbose=None,
        env_file=env_file,
        vlc_url=None,
        vlc_password=None,
        vlc_timeout=None,
        follow=None,
        poll_interval=None,
        resync_threshold=None,
    )


class RunVlcShowEnvTests(unittest.TestCase):
    def test_parse_env_file_supports_export_and_quotes(self):
        with tempfile.TemporaryDirectory() as td:
            env_path = Path(td) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "# comment",
                        "export VLC_HTTP_URL=http://127.0.0.1:8080",
                        "VLC_HTTP_PASSWORD='secret value'",
                        'VLC_HTTP_TIMEOUT="1.5"',
                    ]
                ),
                encoding="utf-8",
            )

            parsed = _parse_env_file(env_path)

        self.assertEqual(parsed["VLC_HTTP_URL"], "http://127.0.0.1:8080")
        self.assertEqual(parsed["VLC_HTTP_PASSWORD"], "secret value")
        self.assertEqual(parsed["VLC_HTTP_TIMEOUT"], "1.5")

    def test_apply_env_defaults_uses_dotenv_for_all_args(self):
        with tempfile.TemporaryDirectory() as td:
            env_path = Path(td) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "RUN_VLC_SHOW_SHOWS_DIR=venue/home-studio/shows",
                        "RUN_VLC_SHOW_IP=10.0.255.255",
                        "RUN_VLC_SHOW_BIND_IP=10.0.0.7",
                        "RUN_VLC_SHOW_UNIVERSE=0",
                        "RUN_VLC_SHOW_PORT=6454",
                        "RUN_VLC_SHOW_BUTTON_ID=11",
                        "RUN_VLC_SHOW_BUTTON_CAPTION=FULL SHOW",
                        "RUN_VLC_SHOW_FUNCTION_ID=42",
                        "RUN_VLC_SHOW_FPS=50",
                        "RUN_VLC_SHOW_MAX_SECONDS=12.5",
                        "RUN_VLC_SHOW_DRY_RUN=true",
                        "RUN_VLC_SHOW_VERBOSE=false",
                        "RUN_VLC_SHOW_VLC_URL=http://127.0.0.1:8080",
                        "RUN_VLC_SHOW_VLC_PASSWORD=from-dotenv",
                        "RUN_VLC_SHOW_VLC_TIMEOUT=2.25",
                        "RUN_VLC_SHOW_FOLLOW=true",
                        "RUN_VLC_SHOW_POLL_INTERVAL=0.2",
                        "RUN_VLC_SHOW_RESYNC_THRESHOLD=0.8",
                    ]
                ),
                encoding="utf-8",
            )

            args = _blank_args(str(env_path))
            with patch.dict("os.environ", {}, clear=True):
                _apply_env_defaults(args)

        self.assertEqual(args.shows_dir, "venue/home-studio/shows")
        self.assertEqual(args.ip, "10.0.255.255")
        self.assertEqual(args.bind_ip, "10.0.0.7")
        self.assertEqual(args.universe, 0)
        self.assertEqual(args.port, 6454)
        self.assertEqual(args.button_id, 11)
        self.assertEqual(args.button_caption, "FULL SHOW")
        self.assertEqual(args.function_id, 42)
        self.assertEqual(args.fps, 50)
        self.assertEqual(args.max_seconds, 12.5)
        self.assertTrue(args.dry_run)
        self.assertFalse(args.verbose)
        self.assertEqual(args.vlc_url, "http://127.0.0.1:8080")
        self.assertEqual(args.vlc_password, "from-dotenv")
        self.assertEqual(args.vlc_timeout, 2.25)
        self.assertTrue(args.follow)
        self.assertEqual(args.poll_interval, 0.2)
        self.assertEqual(args.resync_threshold, 0.8)

    def test_precedence_cli_over_env_over_dotenv(self):
        with tempfile.TemporaryDirectory() as td:
            env_path = Path(td) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "RUN_VLC_SHOW_IP=10.0.0.255",
                        "RUN_VLC_SHOW_FPS=30",
                        "RUN_VLC_SHOW_DRY_RUN=false",
                        "RUN_VLC_SHOW_VLC_URL=http://from-dotenv",
                        "RUN_VLC_SHOW_VLC_PASSWORD=from-dotenv",
                        "RUN_VLC_SHOW_VLC_TIMEOUT=9",
                    ]
                ),
                encoding="utf-8",
            )

            args = _blank_args(str(env_path))
            args.ip = "10.1.1.1"
            args.fps = 44
            args.dry_run = True
            args.vlc_url = "http://from-cli"
            args.vlc_password = "from-cli"
            args.vlc_timeout = 7.0

            with patch.dict(
                "os.environ",
                {
                    "RUN_VLC_SHOW_FPS": "55",
                    "RUN_VLC_SHOW_PORT": "7000",
                    "VLC_HTTP_URL": "http://from-env",
                    "VLC_HTTP_PASSWORD": "from-env",
                    "VLC_HTTP_TIMEOUT": "5.5",
                },
                clear=True,
            ):
                _apply_env_defaults(args)

        self.assertEqual(args.ip, "10.1.1.1")
        self.assertEqual(args.fps, 44)
        self.assertTrue(args.dry_run)
        self.assertEqual(args.port, 7000)
        self.assertEqual(args.vlc_url, "http://from-cli")
        self.assertEqual(args.vlc_password, "from-cli")
        self.assertEqual(args.vlc_timeout, 7.0)

    def test_legacy_vlc_env_names_still_work(self):
        with tempfile.TemporaryDirectory() as td:
            env_path = Path(td) / ".env"
            env_path.write_text("", encoding="utf-8")

            args = _blank_args(str(env_path))
            with patch.dict(
                "os.environ",
                {
                    "VLC_HTTP_URL": "http://legacy",
                    "VLC_HTTP_PASSWORD": "legacy-secret",
                    "VLC_HTTP_TIMEOUT": "3.5",
                },
                clear=True,
            ):
                _apply_env_defaults(args)

        self.assertEqual(args.vlc_url, "http://legacy")
        self.assertEqual(args.vlc_password, "legacy-secret")
        self.assertEqual(args.vlc_timeout, 3.5)

    def test_env_file_can_chain_when_not_cli_locked(self):
        with tempfile.TemporaryDirectory() as td:
            root_env = Path(td) / ".env"
            chained_env = Path(td) / ".env.local"
            root_env.write_text(
                "\n".join(
                    [
                        f"RUN_VLC_SHOW_ENV_FILE={chained_env}",
                        "RUN_VLC_SHOW_SHOWS_DIR=from-root",
                    ]
                ),
                encoding="utf-8",
            )
            chained_env.write_text(
                "\n".join(
                    [
                        "RUN_VLC_SHOW_SHOWS_DIR=from-chain",
                        "RUN_VLC_SHOW_FPS=77",
                    ]
                ),
                encoding="utf-8",
            )

            args = _blank_args(str(root_env))
            with patch.dict("os.environ", {}, clear=True):
                _apply_env_defaults(args, env_file_from_cli=False)

        self.assertEqual(args.env_file, str(chained_env))
        self.assertEqual(args.shows_dir, "from-chain")
        self.assertEqual(args.fps, 77)

    def test_blank_values_are_treated_as_unset(self):
        with tempfile.TemporaryDirectory() as td:
            env_path = Path(td) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "RUN_VLC_SHOW_SHOWS_DIR=venue/home-studio/shows",
                        "RUN_VLC_SHOW_UNIVERSE=",
                        "RUN_VLC_SHOW_PORT=",
                        "RUN_VLC_SHOW_BUTTON_ID=",
                        "RUN_VLC_SHOW_MAX_SECONDS=",
                        "RUN_VLC_SHOW_DRY_RUN=",
                    ]
                ),
                encoding="utf-8",
            )

            args = _blank_args(str(env_path))
            with patch.dict("os.environ", {}, clear=True):
                _apply_env_defaults(args)

        self.assertEqual(args.shows_dir, "venue/home-studio/shows")
        self.assertIsNone(args.universe)
        self.assertEqual(args.port, 6454)
        self.assertIsNone(args.button_id)
        self.assertIsNone(args.max_seconds)
        self.assertFalse(args.dry_run)

    def test_invalid_values_raise(self):
        with tempfile.TemporaryDirectory() as td:
            env_path = Path(td) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "RUN_VLC_SHOW_DRY_RUN=maybe",
                        "RUN_VLC_SHOW_VLC_TIMEOUT=nope",
                    ]
                ),
                encoding="utf-8",
            )
            args = _blank_args(str(env_path))

            with patch.dict("os.environ", {}, clear=True):
                with self.assertRaises(ValueError):
                    _apply_env_defaults(args)


if __name__ == "__main__":
    unittest.main()
