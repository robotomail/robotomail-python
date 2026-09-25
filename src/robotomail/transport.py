"""HTTP transport. No automatic retries, including ambiguous send failures."""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
from dataclasses import dataclass
from typing import Any, AsyncIterator, Iterator, Optional
from urllib.parse import quote, urlsplit

import httpx


@dataclass(frozen=True)
class Upload:
    data: bytes
    filename: str
    content_type: str = "application/octet-stream"


@dataclass(frozen=True)
class EventFrame:
    data: str
    event: str = "message"
    id: Optional[str] = None


class ApiError(Exception):
    def __init__(self, status: int, body: Any, headers: httpx.Headers):
        self.status = status
        self.body = body
        self.headers = headers
        self.code = body.get("code") if isinstance(body, dict) else None
        message = body.get("error") if isinstance(body, dict) else None
        super().__init__(message or f"Robotomail HTTP {status}")


def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    """Verify the original bytes before JSON parsing. Do not reserialize a body."""
    if not secret or not re.fullmatch(r"[0-9a-f]{64}", signature):
        return False
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


class _Parser:
    def __init__(self):
        self.data: list[str] = []
        self.event = "message"
        self.id: Optional[str] = None
        self.size = 0

    def feed(self, line: str) -> Optional[EventFrame]:
        self.size += len(line)
        if self.size > 1024 * 1024:
            raise ValueError("SSE event exceeds 1 MB")
        if line == "":
            frame = EventFrame("\n".join(self.data), self.event, self.id) if self.data else None
            self.data, self.event, self.size = [], "message", 0
            return frame
        key, _, value = line.partition(":")
        if value.startswith(" "):
            value = value[1:]
        if key == "data":
            self.data.append(value)
        elif key == "event":
            self.event = value
        elif key == "id" and "\0" not in value:
            self.id = value
        return None


class _Base:
    def __init__(self, api_key: Optional[str] = None, *, base_url: str = "https://api.robotomail.com/v1",
                 timeout: float = 30.0, transport: Any = None):
        url = urlsplit(base_url)
        if (url.username or url.password or url.query or url.fragment or not url.hostname or
            not (url.scheme == "https" or (url.scheme == "http" and url.hostname in {"localhost", "127.0.0.1", "::1"}))):
            raise ValueError("base_url must be HTTPS, or HTTP on localhost, without credentials, query or fragment")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key if api_key is not None else os.getenv("ROBOTOMAIL_API_KEY")
        self._timeout = timeout
        self._transport = transport

    @staticmethod
    def _segment(value: str) -> str:
        if not value or value in {".", ".."}:
            raise ValueError("Resource IDs must be nonempty path segments")
        return quote(value, safe="")

    def _prepare(self, params=None, stream=False):
        headers = {"Accept": "text/event-stream" if stream else "application/json", "User-Agent": "robotomail-python/0.2.0"}
        if self._api_key:
            headers["Authorization"] = "Bearer " + self._api_key
        query = {}
        for key, value in (params or {}).items():
            if value is None:
                continue
            if key == "Last-Event-ID":
                headers[key] = str(value)
            else:
                query[key] = value
        return headers, query

    @staticmethod
    def _files(file):
        if file is None:
            return None
        if any(char in file.filename + file.content_type for char in "\r\n"):
            raise ValueError("Invalid filename or content type")
        if len(file.data) > 25 * 1024 * 1024:
            raise ValueError("Attachments must be at most 25 MB")
        return {"file": (file.filename, file.data, file.content_type)}

    @staticmethod
    def _decode(response):
        try:
            body = response.json() if response.content else None
        except ValueError:
            if response.is_success:
                raise ValueError("Robotomail returned invalid JSON") from None
            body = response.text
        if not response.is_success:
            raise ApiError(response.status_code, body, response.headers)
        return body


class SyncTransport(_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._http = httpx.Client(timeout=self._timeout, follow_redirects=False, transport=self._transport)

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def _request(self, method, path, body=None, params=None, file=None):
        headers, query = self._prepare(params)
        response = self._http.request(method, self._base_url + path, headers=headers, params=query,
                                      json=body, files=self._files(file))
        return self._decode(response)

    def _stream(self, params=None) -> Iterator[EventFrame]:
        headers, query = self._prepare(params, stream=True)
        parser = _Parser()
        with self._http.stream("GET", self._base_url + "/events", headers=headers, params=query,
                               timeout=httpx.Timeout(self._timeout, read=max(self._timeout, 60))) as response:
            if not response.is_success:
                response.read()
                self._decode(response)
            if not response.headers.get("content-type", "").startswith("text/event-stream"):
                raise ValueError("Robotomail returned a non-SSE response")
            for line in response.iter_lines():
                frame = parser.feed(line)
                if frame is not None:
                    yield frame


class AsyncTransport(_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._http = httpx.AsyncClient(timeout=self._timeout, follow_redirects=False, transport=self._transport)

    async def close(self):
        await self._http.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()

    async def _request(self, method, path, body=None, params=None, file=None):
        headers, query = self._prepare(params)
        response = await self._http.request(method, self._base_url + path, headers=headers, params=query,
                                            json=body, files=self._files(file))
        return self._decode(response)

    async def _stream(self, params=None) -> AsyncIterator[EventFrame]:
        headers, query = self._prepare(params, stream=True)
        parser = _Parser()
        async with self._http.stream("GET", self._base_url + "/events", headers=headers, params=query,
                                     timeout=httpx.Timeout(self._timeout, read=max(self._timeout, 60))) as response:
            if not response.is_success:
                await response.aread()
                self._decode(response)
            if not response.headers.get("content-type", "").startswith("text/event-stream"):
                raise ValueError("Robotomail returned a non-SSE response")
            async for line in response.aiter_lines():
                frame = parser.feed(line)
                if frame is not None:
                    yield frame
