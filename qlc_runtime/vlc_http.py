#!/usr/bin/env python3
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import unquote, urlparse
from urllib.request import (
    HTTPBasicAuthHandler,
    HTTPPasswordMgrWithDefaultRealm,
    Request,
    build_opener,
    urlopen,
)


DEFAULT_VLC_URL = "http://127.0.0.1:8080"
STATUS_PATH = "/requests/status.json"


@dataclass
class VlcStatus:
    state: str
    time_s: float
    length_s: Optional[float]
    media_uri: Optional[str]
    filename: Optional[str]
    title: Optional[str]
    position_ratio: Optional[float] = None


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _as_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _status_url(base_url: str) -> str:
    root = str(base_url or DEFAULT_VLC_URL).rstrip("/")
    if root.endswith(STATUS_PATH):
        return root
    return f"{root}{STATUS_PATH}"


def parse_vlc_status_payload(payload: Dict[str, Any]) -> VlcStatus:
    info = payload.get("information")
    categories = info.get("category") if isinstance(info, dict) else None
    meta = categories.get("meta") if isinstance(categories, dict) else None
    if not isinstance(meta, dict):
        meta = {}

    media_uri = _as_str(meta.get("url") or payload.get("uri"))
    filename = _as_str(meta.get("filename"))
    title = _as_str(meta.get("title"))
    position_ratio = None
    raw_position = payload.get("position")
    if raw_position is not None:
        try:
            position_ratio = max(0.0, min(1.0, float(raw_position)))
        except (TypeError, ValueError):
            position_ratio = None

    return VlcStatus(
        state=str(payload.get("state") or "").strip().casefold(),
        time_s=max(0.0, _to_float(payload.get("time"), 0.0)),
        length_s=max(0.0, _to_float(payload.get("length"), 0.0)) if payload.get("length") is not None else None,
        media_uri=media_uri,
        filename=filename,
        title=title,
        position_ratio=position_ratio,
    )


def get_vlc_status(base_url: str, password: Optional[str], timeout_s: float = 1.0) -> VlcStatus:
    status_url = _status_url(base_url)
    request = Request(status_url, headers={"Accept": "application/json"})

    if password is None:
        with urlopen(request, timeout=timeout_s) as resp:
            payload = json.load(resp)
        return parse_vlc_status_payload(payload)

    manager = HTTPPasswordMgrWithDefaultRealm()
    manager.add_password(None, status_url, "", password)
    opener = build_opener(HTTPBasicAuthHandler(manager))
    with opener.open(request, timeout=timeout_s) as resp:
        payload = json.load(resp)
    return parse_vlc_status_payload(payload)


def _basename_from_uri(uri: str) -> Optional[str]:
    if not uri:
        return None
    parsed = urlparse(uri)
    candidate = uri
    if parsed.scheme:
        if parsed.scheme == "file":
            candidate = unquote(parsed.path or "")
            if parsed.netloc:
                candidate = f"/{parsed.netloc}{candidate}"
        else:
            candidate = unquote(parsed.path or "")
    candidate = candidate.replace("\\", "/").strip()
    if not candidate:
        return None
    return Path(candidate).name or None


def extract_media_basename(status: VlcStatus) -> Optional[str]:
    from_uri = _basename_from_uri(status.media_uri or "")
    if from_uri:
        return from_uri
    if status.filename:
        return status.filename
    if status.title:
        return status.title
    return None
