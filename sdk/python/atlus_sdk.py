"""Atlus for your own agent - one file, no dependencies beyond the standard library.

    from atlus_sdk import Atlus
    atlus = Atlus("atl_key_...")                      # a key from Settings -> Keys for your agents
    print(atlus.my_agent())                            # name, cost mode, shared instructions
    print(atlus.recall("weekly report"))               # notes the person shared with their AIs
    job = atlus.draft_email(to="ana@example.com", subject="Thursday", body="See you at 10.")
    print(atlus.job(job["mission_id"], wait_seconds=20))

Every call is a tool on the Atlus MCP server (https://vonit.si/mcp). Atlus never
gives your agent the person's passwords or tokens; sending, booking and paying
always wait for the person's approval in Atlus. Verify callbacks with
`Atlus.verify_callback`.
"""

from __future__ import annotations

import hashlib
import hmac
import itertools
import json
import time
import urllib.error
import urllib.request
from typing import Any

PROTOCOL = "2026-07-28"
__version__ = "0.1.0"


class AtlusError(Exception):
    """A refusal or failure Atlus explained; `str(error)` says what to do."""


class Atlus:
    def __init__(self, key: str, url: str = "https://vonit.si", timeout: float = 60.0):
        if not key.startswith("atl_key_"):
            raise ValueError("an Atlus key starts with atl_key_ (Settings -> Keys for your agents)")
        self._key, self._url, self._timeout = key, url.rstrip("/") + "/mcp", timeout
        self._ids = itertools.count(1)

    # ------------------------------------------------------------------ tools
    def call(self, tool: str, **arguments: Any) -> dict[str, Any]:
        """Any Atlus tool by name; the helpers below are the common ones."""
        result = self._rpc("tools/call", {"name": tool, "arguments": arguments}, name=tool)
        text = (result.get("content") or [{}])[0].get("text", "")
        if result.get("isError"):
            raise AtlusError(text or f"{tool} was refused")
        return result.get("structuredContent") or (json.loads(text) if text else {})

    def tools(self) -> list[str]:
        return [t["name"] for t in self._rpc("tools/list", {}).get("tools", [])]

    def my_agent(self) -> dict:
        return self.call("my_agent")

    def recall(self, about: str) -> dict:
        return self.call("recall", about=about)

    def remember(self, note: str) -> dict:
        return self.call("remember", note=note)

    def delegate(self, job: str, worker: str | None = None, budget_usd: float | None = None,
                 needs_my_data: bool = False, idempotency_key: str | None = None) -> dict:
        args = {"job": job, "needs_my_data": needs_my_data}
        args.update({k: v for k, v in (("worker", worker), ("budget_usd", budget_usd),
                                       ("idempotency_key", idempotency_key)) if v is not None})
        return self.call("delegate", **args)

    def start(self, outcome: str, budget_usd: float | None = None,
              idempotency_key: str | None = None) -> dict:
        args = {"outcome": outcome}
        args.update({k: v for k, v in (("budget_usd", budget_usd),
                                       ("idempotency_key", idempotency_key)) if v is not None})
        return self.call("start_mission", **args)

    def draft_email(self, subject: str, body: str, to: str | None = None) -> dict:
        return self.call("draft_email", subject=subject, body=body, **({"to": to} if to else {}))

    def send_to_me(self, subject: str, body: str) -> dict:
        return self.call("send_to_me", subject=subject, body=body)

    def job(self, mission_id: str, wait_seconds: int = 0) -> dict:
        return self.call("job", mission_id=mission_id, wait_seconds=wait_seconds)

    def wait(self, mission_id: str, timeout: float = 600.0) -> dict:
        """Follow a job until it ends or needs the person (then give them its link)."""
        end = time.monotonic() + timeout
        while True:
            state = self.job(mission_id, wait_seconds=20)
            if state.get("ended") or state.get("waiting_for") or time.monotonic() > end:
                return state

    # -------------------------------------------------------------- callbacks
    @staticmethod
    def verify_callback(secret: str, timestamp: str, body: bytes, signature: str,
                        max_age: float = 300.0) -> bool:
        """True when a callback is Atlus's: the x-atlus-signature over
        "<x-atlus-timestamp>.<raw body>" with your key's callback secret, and fresh."""
        if abs(time.time() - float(timestamp)) > max_age:
            return False
        expected = "sha256=" + hmac.new(secret.encode(), timestamp.encode() + b"." + body,
                                        hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    # --------------------------------------------------------------- protocol
    def _rpc(self, method: str, params: dict, *, name: str | None = None) -> dict:
        params = {**params, "_meta": {
            "io.modelcontextprotocol/protocolVersion": PROTOCOL,
            "io.modelcontextprotocol/clientInfo": {"name": "atlus-sdk-python", "version": __version__},
            "io.modelcontextprotocol/clientCapabilities": {}}}
        headers = {"authorization": f"Bearer {self._key}", "content-type": "application/json",
                   "accept": "application/json, text/event-stream",
                   "mcp-protocol-version": PROTOCOL, "mcp-method": method}
        if name:
            headers["mcp-name"] = name
        body = json.dumps({"jsonrpc": "2.0", "id": next(self._ids), "method": method,
                           "params": params}).encode()
        request = urllib.request.Request(self._url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as answered:
                reply = json.loads(answered.read().decode())
        except urllib.error.HTTPError as failed:
            detail = failed.read().decode(errors="replace")[:300]
            if failed.code == 401:
                raise AtlusError("the key was not accepted - revoked or mistyped") from None
            if failed.code == 403:
                raise AtlusError("this key is not allowed that - the person can widen it in "
                                 "Settings -> Keys for your agents") from None
            raise AtlusError(f"Atlus answered {failed.code}: {detail}") from None
        if "error" in reply:
            raise AtlusError(str(reply["error"].get("message") or reply["error"]))
        return reply.get("result") or {}


__all__ = ["Atlus", "AtlusError"]
