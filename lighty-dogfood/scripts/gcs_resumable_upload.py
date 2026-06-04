#!/usr/bin/env python3
"""Resumable upload of a (large) local file to a GCS resumable signed URL.

Stdlib only — ships inside the lighty-dogfood plugin and runs on the user's
machine, so it must not import anything outside the standard library.

Survives a flaky connection: catches both HTTP error statuses AND real
connection drops/timeouts (URLError/OSError), re-queries the committed offset,
and resumes — with a per-chunk retry budget (reset on progress) and backoff.

CLI:  python gcs_resumable_upload.py <file> <signed_url>
"""

from __future__ import annotations

import os
import sys
import time
import urllib.error
import urllib.request

CHUNK = 8 * 1024 * 1024  # 8 MiB (multiple of 256 KiB)
TIMEOUT = 120  # seconds — so a half-open socket fails fast instead of hanging


def _request(method, url, *, data=None, headers=None, timeout=TIMEOUT):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    return urllib.request.urlopen(req, timeout=timeout)  # noqa: S310 — trusted signed URL


def _offset_from_range(headers):
    rng = headers.get("Range")
    if rng and "-" in rng:
        return int(rng.split("-")[1]) + 1
    return None


def _human(n):
    f = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if f < 1024 or unit == "TB":
            return f"{int(n)}B" if unit == "B" else f"{f:.1f}{unit}"
        f /= 1024
    return f"{n}B"


def _initiate(signed_url):
    resp = _request(
        "POST",
        signed_url,
        data=b"",
        headers={"x-goog-resumable": "start", "Content-Length": "0"},
    )
    loc = resp.headers.get("Location")
    if not loc:
        raise RuntimeError("resumable initiate did not return a session Location")
    return loc


def _committed_offset(session_uri, total):
    """Authoritative committed byte count from the session (total if complete)."""
    try:
        _request("PUT", session_uri, data=b"", headers={"Content-Range": f"bytes */{total}"})
        return total  # 2xx => already complete
    except urllib.error.HTTPError as e:
        if e.code == 308:
            return _offset_from_range(e.headers) or 0
        raise


def resumable_upload(file_path, signed_url, *, chunk_size=CHUNK, max_retries=5):
    """Upload file_path to a GCS resumable signed URL; returns {bytes_sent}."""
    if chunk_size % (256 * 1024):
        raise ValueError("chunk_size must be a multiple of 256 KiB")
    total = os.path.getsize(file_path)
    started = time.monotonic()
    session = _initiate(signed_url)

    if total == 0:  # finalize a zero-byte object
        try:
            _request("PUT", session, data=b"", headers={"Content-Range": "bytes */0"})
        except urllib.error.HTTPError as e:
            if e.code not in (200, 201):
                raise
        return {"bytes_sent": 0}

    def _progress(sent):
        pct = 100.0 * sent / total
        print(
            f"  uploaded {_human(sent)}/{_human(total)} ({pct:.1f}%) · "
            f"elapsed {int(time.monotonic() - started)}s",
            flush=True,
        )

    sent = 0
    attempts = 0  # per-position; reset on forward progress
    with open(file_path, "rb") as fh:
        while sent < total:
            fh.seek(sent)
            chunk = fh.read(chunk_size)
            end = sent + len(chunk) - 1
            headers = {
                "Content-Length": str(len(chunk)),
                "Content-Range": f"bytes {sent}-{end}/{total}",
            }
            try:
                resp = _request("PUT", session, data=chunk, headers=headers)
            except urllib.error.HTTPError as e:
                if e.code == 308:  # normal: chunk accepted, keep going
                    sent = _offset_from_range(e.headers) or (end + 1)
                    attempts = 0
                    _progress(sent)
                    continue
                sent, attempts = _retry(session, total, attempts, max_retries)
                continue
            except (urllib.error.URLError, OSError):  # real connection drop / timeout
                sent, attempts = _retry(session, total, attempts, max_retries)
                continue
            # success (no exception)
            sent = (
                total
                if resp.status in (200, 201)
                else (_offset_from_range(resp.headers) or end + 1)
            )
            attempts = 0
            _progress(sent)
    return {"bytes_sent": total}


def _retry(session, total, attempts, max_retries):
    """Handle a transient failure: bounded backoff, then re-sync to the
    server's committed offset. Raises once the per-chunk budget is spent."""
    attempts += 1
    if attempts > max_retries:
        raise RuntimeError(f"upload failed after {max_retries} retries at this position")
    delay = min(2**attempts, 30)
    print(
        f"  connection blipped — resyncing + retrying in {delay}s "
        f"(attempt {attempts}/{max_retries})…",
        flush=True,
    )
    time.sleep(delay)
    return _committed_offset(session, total), attempts


def main(argv):
    if len(argv) != 3:
        print("usage: gcs_resumable_upload.py <file> <signed_url>", file=sys.stderr)
        return 2
    result = resumable_upload(argv[1], argv[2])
    print(f"done: {result['bytes_sent']} bytes", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
