import asyncio
import hashlib
import hmac
import json
import re
import subprocess
import sys
from pathlib import Path

import httpx
import pytest
from robotomail import Robotomail, AsyncRobotomail, ApiError, Upload, verify_webhook

CASES = json.loads((Path(__file__).parent / "cases.json").read_text())


@pytest.fixture(scope="module")
def base_url():
    proc = subprocess.Popen([sys.executable, str(Path(__file__).parent / "server.py")], stdout=subprocess.PIPE, text=True)
    url = proc.stdout.readline().strip()
    assert url.startswith("http://127.0.0.1:")
    yield url
    proc.terminate()
    proc.wait(timeout=5)


def method(name):
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def arguments(case):
    args = list(case["paths"])
    if case["body"] is not None:
        args.append(case["body"])
    if case["upload"]:
        args.append(Upload(b"\x00\xffbinary\r\n", "sample.bin"))
    if case["params"]:
        args.append(case["params"])
    return args


def check_frames(frames):
    assert [(f.id, f.event, f.data) for f in frames] == [
        ("evt-1", "message.received", '{"text":\n"héllo"}'),
        ("evt-1", "message", "second"), ("evt-2", "reconnect", "{}")]


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_sync_contract(base_url, case):
    with Robotomail("test-key", base_url=base_url) as client:
        result = getattr(client, method(case["id"]))(*arguments(case))
        if case["id"] == "streamEvents":
            check_frames(list(result))
        else:
            assert result == case["response"]


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_async_contract(base_url, case):
    async def run():
        async with AsyncRobotomail("test-key", base_url=base_url) as client:
            result = getattr(client, method(case["id"]))(*arguments(case))
            if case["id"] == "streamEvents":
                check_frames([frame async for frame in result])
            else:
                assert await result == case["response"]
    asyncio.run(run())


@pytest.mark.parametrize("status", [401, 402, 403, 404, 429, 500])
def test_errors(base_url, status):
    with Robotomail(f"error-{status}", base_url=base_url) as client:
        with pytest.raises(ApiError) as caught:
            client.list_mailboxes()
        assert caught.value.status == status
        assert caught.value.code == "FIXTURE_ERROR"
        assert caught.value.headers["retry-after"] == "7"


def test_redirects_and_timeouts(base_url):
    with Robotomail("redirect", base_url=base_url) as client:
        with pytest.raises(ApiError) as caught:
            client.send_message("box", {"to": ["fixture@example.com"], "subject": "fixture", "bodyText": "fixture"})
        assert caught.value.status == 307
    with Robotomail("slow", base_url=base_url, timeout=0.015) as client:
        with pytest.raises(httpx.TimeoutException):
            client.list_mailboxes()
    requests = httpx.get(base_url.replace("/v1", "/__requests")).json()
    assert sum(r["auth"] == "Bearer redirect" for r in requests) == 1
    assert not any(r["path"] == "/__unexpected" for r in requests)


def test_null_empty_and_zero(base_url):
    with Robotomail("echo", base_url=base_url) as client:
        assert client.update_webhook("hook", {})["echo"] == {}
        assert client.update_webhook("hook", {"headers": None})["echo"] == {"headers": None}
        assert client.update_mailbox("box", {"displayName": ""})["echo"] == {"displayName": ""}
        assert client.list_messages("box", {"limit": 2, "offset": 0})["query"]["offset"] == ["0"]


def test_webhooks():
    raw, secret = '{"text":"héllo"}\n'.encode(), "fixture-secret"
    signature = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
    assert verify_webhook(raw, signature, secret)
    for bad in ["", signature.upper(), "g" * 64, signature + "0"]:
        assert not verify_webhook(raw, bad, secret)
    assert not verify_webhook(raw.strip(), signature, secret)
    assert not verify_webhook(raw, signature, "wrong")


def test_stream_cleanup_and_bad_content(base_url):
    params = next(c["params"] for c in CASES if c["id"] == "streamEvents")
    with Robotomail("test-key", base_url=base_url) as client:
        iterator = client.stream_events(params)
        assert next(iterator).id == "evt-1"
        iterator.close()
    with Robotomail("bad-stream", base_url=base_url) as client:
        with pytest.raises(ValueError, match="non-SSE"):
            list(client.stream_events(params))
    async def run():
        async with AsyncRobotomail("test-key", base_url=base_url) as client:
            iterator = client.stream_events(params)
            assert (await anext(iterator)).id == "evt-1"
            await iterator.aclose()
    asyncio.run(run())


def test_url_validation():
    for url in ["http://example.com/v1", "https://user:pass@example.com/v1", "https://example.com/v1?key=x"]:
        with pytest.raises(ValueError):
            Robotomail(base_url=url)
    for value in ["", ".", ".."]:
        with pytest.raises(ValueError):
            Robotomail._segment(value)


def test_upload_rejects_header_injection():
    with pytest.raises(ValueError, match="Invalid filename or content type"):
        Robotomail._files(Upload(b"fixture", "sample.bin", "text/plain\r\nInjected: header"))
