"""Version comparison and release parsing for the GitHub update check."""

from __future__ import annotations

import ssl

import pytest

from refview.core import update_check
from refview.core.update_check import (
    RELEASES_PAGE,
    Release,
    UpdateCheckError,
    is_newer,
    parse_version,
    release_from_payload,
    trusted_roots,
)


def test_the_release_check_trusts_a_certificate_bundle():
    """Whatever the interpreter was built with, the context has roots in it."""
    context = trusted_roots()
    assert isinstance(context, ssl.SSLContext)
    assert context.verify_mode is ssl.CERT_REQUIRED
    assert context.cert_store_stats()["x509"] > 0


def test_the_fetch_hands_urlopen_the_trusted_context(monkeypatch):
    seen = {}

    class _Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return b'{"tag_name": "v9.9.9", "html_url": "https://example.test/r"}'

    def fake_urlopen(request, timeout, context):
        seen["context"] = context
        return _Response()

    monkeypatch.setattr(update_check.urllib.request, "urlopen", fake_urlopen)
    release = update_check.fetch_latest_release()
    assert release == Release("9.9.9", "https://example.test/r")
    assert isinstance(seen["context"], ssl.SSLContext)


def test_a_certificate_failure_is_reported_not_raised(monkeypatch):
    def failing(request, timeout, context):
        raise ssl.SSLCertVerificationError("unable to get local issuer certificate")

    monkeypatch.setattr(update_check.urllib.request, "urlopen", failing)
    with pytest.raises(UpdateCheckError, match="local issuer"):
        update_check.fetch_latest_release()


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1.1.2", (1, 1, 2)),
        ("v1.1.2", (1, 1, 2)),
        ("  v2.0  ", (2, 0)),
        ("1.2.0-rc1", (1, 2, 0, -1)),
        ("nightly", None),
        ("", None),
    ],
)
def test_parse_version(text, expected):
    assert parse_version(text) == expected


@pytest.mark.parametrize(
    ("candidate", "current", "expected"),
    [
        ("1.1.3", "1.1.2", True),
        ("1.2.0", "1.1.9", True),
        ("2.0", "1.9.9", True),
        ("1.1.2", "1.1.2", False),
        ("1.1.1", "1.1.2", False),
        # A trailing zero is not a new release.
        ("1.1", "1.1.0", False),
        ("1.1.0", "1.1", False),
        # A pre-release loses to the final release of the same number.
        ("1.1.3-rc1", "1.1.3", False),
        ("1.1.3-rc1", "1.1.2", True),
        ("garbage", "1.1.2", False),
    ],
)
def test_is_newer(candidate, current, expected):
    assert is_newer(candidate, current) is expected


def test_release_from_payload_strips_the_tag_prefix():
    release = release_from_payload(
        {"tag_name": "v1.2.0", "html_url": "https://example.invalid/releases/v1.2.0"}
    )
    assert release == Release(version="1.2.0", url="https://example.invalid/releases/v1.2.0")


def test_release_falls_back_to_the_releases_page():
    assert release_from_payload({"tag_name": "v1.2.0"}).url == RELEASES_PAGE


@pytest.mark.parametrize("payload", [{}, {"tag_name": "nightly"}, [], None])
def test_unusable_payloads_are_reported(payload):
    with pytest.raises(UpdateCheckError):
        release_from_payload(payload)
