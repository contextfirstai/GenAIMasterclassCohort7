"""Tests for the connection diagnostic's pure classification logic."""
from __future__ import annotations

import pytest

from diagnose_connection import classify_url, explain_error


@pytest.mark.parametrize(
    "url,expected",
    [
        ("", "empty"),
        ("xyz.cloud.qdrant.io", "no-scheme"),
        ("http://xyz.cloud.qdrant.io:6333", "insecure-cloud"),
        ("https://xyz.cloud.qdrant.io:6334", "grpc-port"),
        ("https://xyz.cloud.qdrant.io:6333", "ok"),
        ("https://xyz.cloud.qdrant.io", "ok"),
        ("http://localhost:6333", "ok"),
    ],
)
def test_classify_url(url, expected):
    assert classify_url(url) == expected


def test_explain_error_maps_connection_reset():
    msg = explain_error(ConnectionResetError(54, "Connection reset by peer"))
    assert "reset" in msg.lower()
    assert "6334" in msg or "scheme" in msg.lower() or "paused" in msg.lower()


def test_explain_error_is_generic_for_unknown():
    assert explain_error(ValueError("boom")) != ""
