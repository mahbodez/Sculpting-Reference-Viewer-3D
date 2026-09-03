"""Version comparison and release parsing for the GitHub update check."""

from __future__ import annotations

import pytest

from refview.core.update_check import (
    RELEASES_PAGE,
    Release,
    UpdateCheckError,
    is_newer,
    parse_version,
    release_from_payload,
)


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
