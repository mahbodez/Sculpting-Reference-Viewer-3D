"""Ask GitHub whether a newer release exists.

The check is deliberately small and dependency-free: one JSON request to the
public releases endpoint, a tolerant version comparison and a link to the
release page.  Nothing here touches Qt, so it can be tested on its own and run
off the UI thread.
"""

from __future__ import annotations

import contextlib
import json
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass

REPOSITORY = "mahbodez/Sculpting-Reference-Viewer-3D"
LATEST_RELEASE_API = f"https://api.github.com/repos/{REPOSITORY}/releases/latest"
RELEASES_PAGE = f"https://github.com/{REPOSITORY}/releases/latest"

#: Releases are tagged ``v1.2.3``; drafts and pre-releases carry a suffix.
_VERSION_PATTERN = re.compile(r"^\s*v?(\d+(?:\.\d+)*)(.*)$")

_TIMEOUT_SECONDS = 6.0

#: Where macOS keeps the root certificates every other application trusts.
_MACOS_ROOTS = "/System/Library/Keychains/SystemRootCertificates.keychain"


class UpdateCheckError(RuntimeError):
    """The release could not be looked up (offline, rate limited, malformed)."""


@dataclass(frozen=True)
class Release:
    """The newest published release, as GitHub describes it."""

    version: str
    url: str


def parse_version(text: str) -> tuple[int, ...] | None:
    """Numeric components of ``text``, or ``None`` when it is not a version.

    A pre-release suffix (``1.2.0-rc1``) sorts before the matching final
    release, which is what appending ``-1`` to the tuple achieves.
    """
    match = _VERSION_PATTERN.match(text)
    if match is None:
        return None
    numbers = tuple(int(part) for part in match.group(1).split("."))
    return numbers + (-1,) if match.group(2).strip(" \t") else numbers


def is_newer(candidate: str, current: str) -> bool:
    """Whether ``candidate`` is a strictly later version than ``current``."""
    latest = parse_version(candidate)
    installed = parse_version(current)
    if latest is None or installed is None:
        return False
    # Compare on equal footing so that 1.2 does not read as older than 1.2.0.
    length = max(len(latest), len(installed))
    return _padded(latest, length) > _padded(installed, length)


def _padded(version: tuple[int, ...], length: int) -> tuple[int, ...]:
    return version + (0,) * (length - len(version))


def trusted_roots() -> ssl.SSLContext:
    """A TLS context that can actually verify GitHub's certificate.

    Python's own context trusts whatever OpenSSL was pointed at when it was
    built, which on a Mac -- and in a frozen app on any platform -- can be a
    directory that is not there, so every HTTPS request fails with "unable
    to get local issuer certificate".  The ``certifi`` bundle is the usual
    answer and is used when it is installed; failing that, on a Mac the
    system's own root certificates are read out of the keychain, which is
    what every other application on the machine trusts.
    """
    try:
        import certifi
    except ImportError:
        certifi = None
    if certifi is not None:
        try:
            return ssl.create_default_context(cafile=certifi.where())
        except (OSError, ssl.SSLError):
            pass
    context = ssl.create_default_context()
    if context.cert_store_stats().get("x509", 0) == 0 and sys.platform == "darwin":
        roots = _macos_root_certificates()
        if roots:
            with contextlib.suppress(ssl.SSLError):
                context.load_verify_locations(cadata=roots)
    return context


def _macos_root_certificates() -> str:
    """The system root certificates as PEM text, or ``""`` if they cannot be read."""
    try:
        done = subprocess.run(
            ["security", "find-certificate", "-a", "-p", _MACOS_ROOTS],
            capture_output=True,
            text=True,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return done.stdout if done.returncode == 0 else ""


def fetch_latest_release(timeout: float = _TIMEOUT_SECONDS) -> Release:
    """Return the newest published release, or raise :class:`UpdateCheckError`."""
    request = urllib.request.Request(
        LATEST_RELEASE_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"refview ({REPOSITORY})",
        },
    )
    try:
        context = trusted_roots()
        with urllib.request.urlopen(  # noqa: S310
            request, timeout=timeout, context=context
        ) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
        raise UpdateCheckError(str(error)) from error
    return release_from_payload(payload)


def release_from_payload(payload: object) -> Release:
    """Pull the tag and page link out of a GitHub release document."""
    if not isinstance(payload, dict):
        raise UpdateCheckError("unexpected response from GitHub")
    tag = payload.get("tag_name") or payload.get("name")
    if not isinstance(tag, str) or parse_version(tag) is None:
        raise UpdateCheckError("the latest release has no version tag")
    url = payload.get("html_url")
    return Release(
        version=tag.lstrip("vV").strip(),
        url=url if isinstance(url, str) and url else RELEASES_PAGE,
    )


def check_for_update(current_version: str, timeout: float = _TIMEOUT_SECONDS) -> Release | None:
    """The newest release when it is later than ``current_version``, else ``None``."""
    release = fetch_latest_release(timeout)
    return release if is_newer(release.version, current_version) else None
