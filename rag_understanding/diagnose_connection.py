#!/usr/bin/env python3
"""
diagnose_connection.py — why the RAG demo cannot reach Qdrant or OpenAI
=======================================================================
Run it from the module directory:

    ./.venv/bin/python diagnose_connection.py

It reads the same .env files the app does (see rag_env.py), never prints a
secret in full, and tells you which hop failed and what usually causes it.
"""

from __future__ import annotations

import socket
import ssl
import sys
from urllib.parse import urlparse

from rag_env import (
    get_openai_api_key,
    get_qdrant_api_key,
    get_qdrant_collection,
    get_qdrant_url,
)

CLOUD_HINT = "cloud.qdrant.io"


def classify_url(url: str) -> str:
    """Categorise a Qdrant URL by the mistakes that cause connection resets."""
    if not url.strip():
        return "empty"
    parsed = urlparse(url.strip())
    if not parsed.scheme:
        return "no-scheme"
    if parsed.port == 6334:
        return "grpc-port"
    if parsed.scheme == "http" and CLOUD_HINT in (parsed.hostname or ""):
        return "insecure-cloud"
    return "ok"


def explain_error(exc: BaseException) -> str:
    """Turn a raw socket/SSL error into the cause that usually produces it."""
    text = f"{type(exc).__name__}: {exc}".lower()
    if "reset" in text or "errno 54" in text:
        return (
            "Connection reset by peer. Usual causes, most likely first:\n"
            "  1. The Qdrant Cloud cluster is paused or deleted (free clusters "
            "sleep after inactivity) — check the Qdrant Cloud console.\n"
            "  2. The URL uses port 6334 (gRPC); the REST client needs 6333.\n"
            "  3. The URL uses http:// against an https-only cloud endpoint, so "
            "TLS is refused mid-handshake."
        )
    if "timed out" in text or "timeout" in text:
        return "Timed out — host unreachable, or a firewall is dropping the packets."
    if "name or service not known" in text or "nodename nor servname" in text:
        return "DNS failed — the hostname is wrong or the cluster no longer exists."
    if "certificate" in text or "ssl" in text:
        return "TLS failure — check the scheme and that the endpoint is genuinely https."
    if "401" in text or "forbidden" in text or "unauthorized" in text:
        return "Rejected — the API key is wrong or lacks access to that collection."
    return f"Unrecognised failure: {type(exc).__name__}: {exc}"


def _mask(value: str | None) -> str:
    if not value:
        return "(not set)"
    return f"set, {len(value)} chars, {value[:4]}…{value[-3:]}" if len(value) > 10 else "set (short)"


def _probe_tcp(host: str, port: int, use_tls: bool) -> tuple[bool, str]:
    try:
        with socket.create_connection((host, port), timeout=8) as sock:
            if use_tls:
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(sock, server_hostname=host):
                    return True, "TLS handshake succeeded"
            return True, "TCP connect succeeded"
    except Exception as exc:  # noqa: BLE001 — we report every failure kind
        return False, explain_error(exc)


def main() -> int:
    url = get_qdrant_url()
    print("── Credentials ─────────────────────────────────────────────")
    print(f"  QDRANT_URL        : {url or '(not set)'}")
    print(f"  QDRANT_API_KEY    : {_mask(get_qdrant_api_key())}")
    print(f"  QDRANT_COLLECTION : {get_qdrant_collection()}")
    print(f"  OPENAI_API_KEY    : {_mask(get_openai_api_key())}")

    verdict = classify_url(url)
    print("\n── URL check ───────────────────────────────────────────────")
    messages = {
        "empty": "No Qdrant URL set. Add it to rag_understanding/.env or the sidebar.",
        "no-scheme": "Missing scheme — prefix it with https:// (or http:// for local).",
        "grpc-port": "Port 6334 is the gRPC port. The REST client needs 6333.",
        "insecure-cloud": "Cloud endpoints are https-only; http:// will be reset.",
        "ok": "URL shape looks right.",
    }
    print(f"  {messages[verdict]}")
    if verdict == "empty":
        return 1

    parsed = urlparse(url)
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 6333)
    print("\n── Reachability ────────────────────────────────────────────")
    print(f"  Probing {host}:{port} …")
    ok, detail = _probe_tcp(host, port, use_tls=(parsed.scheme == "https"))
    print(f"  {'OK   ' if ok else 'FAIL '} {detail}")

    if ok:
        print("\n── Qdrant API ──────────────────────────────────────────────")
        try:
            from qdrant_client import QdrantClient

            client = QdrantClient(url=url, api_key=get_qdrant_api_key(), timeout=10)
            names = [c.name for c in client.get_collections().collections]
            print(f"  Collections visible: {names or '(none)'}")
            wanted = get_qdrant_collection()
            if wanted in names:
                info = client.get_collection(wanted)
                print(f"  '{wanted}' exists — points: {info.points_count}")
                if not info.points_count:
                    print("  WARNING: collection is empty — ingest a PDF first.")
            else:
                print(f"  '{wanted}' NOT found — ingest a PDF in the Qdrant PDF lab tab.")
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL  {explain_error(exc)}")
            return 1

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
