"""Helper for calling the workshop's ask-ai API.

ask-ai speaks the OpenAI *chat completions* protocol, so AI features just POST
a prompt and read back text. Use `ask_ai()` instead of hand-rolling the HTTP
call, so auth, the base URL, and error handling stay consistent.

Under Docker, ASKAI_API_BASE_URL points at the `ai-proxy` service, which holds
the token and injects the Authorization header — so the backend runs *without*
ASKAI_API_TOKEN. If a token is present (e.g. native dev calling the API
directly), it's sent as a Bearer header.

Environment (see example.env / .env):
  ASKAI_API_BASE_URL  optional — defaults to https://ask-ai.smartclip.net/api
                                 (Docker sets it to the ai-proxy service)
  ASKAI_API_TOKEN     optional — only needed when calling the API directly
                                 (not via the proxy)
  ASKAI_MODEL         optional — defaults to vllm/generic
                                 (other options: vllm/coding, vllm/deepseek)
"""

import json
import os
from typing import Any

import httpx
from fastapi import HTTPException

BASE_URL = os.environ.get("ASKAI_API_BASE_URL", "https://ask-ai.smartclip.net/api")
DEFAULT_MODEL = os.environ.get("ASKAI_MODEL", "vllm/generic")


def ask_ai(
    prompt: str,
    *,
    system: str | None = None,
    model: str | None = None,
    temperature: float = 0.7,
    timeout: float = 60.0,
    response_format: dict | None = None,
) -> str:
    """Send a prompt to ask-ai and return the model's text reply.

    `system` is an optional instruction that steers the model (e.g. "You are a
    concise chef."). `response_format` is passed straight through — e.g.
    `{"type": "json_object"}` to request JSON (see `ask_ai_json`). Raises
    HTTPException(502) so upstream failures surface cleanly from a route.
    """
    # The proxy adds auth, so a token is optional. Send it only if we have one
    # (native/direct calls); otherwise rely on ASKAI_API_BASE_URL (the proxy).
    headers = {}
    token = os.environ.get("ASKAI_API_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload: dict[str, Any] = {
        "model": model or DEFAULT_MODEL,
        "messages": messages,
        "temperature": temperature,
    }
    if response_format is not None:
        payload["response_format"] = response_format

    try:
        response = httpx.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=timeout,
            follow_redirects=True,
        )
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"ask-ai request failed: {exc}") from exc

    return data["choices"][0]["message"]["content"]


def ask_ai_json(
    prompt: str,
    *,
    system: str | None = None,
    model: str | None = None,
    temperature: float = 0.2,
    timeout: float = 60.0,
) -> Any:
    """Ask ask-ai for JSON and return it parsed.

    Requests JSON mode (`response_format={"type": "json_object"}`) and parses the
    reply. Models sometimes wrap JSON in prose or ``` fences, so we fall back to
    extracting the outermost `{...}`. Validate the result against a Pydantic
    model in the route (see /api/ai/generate-recipe). Use a low temperature for
    more deterministic structure. Raises HTTPException(502) on invalid JSON.
    """
    text = ask_ai(
        prompt,
        system=system,
        model=model,
        temperature=temperature,
        timeout=timeout,
        response_format={"type": "json_object"},
    )
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
        raise HTTPException(status_code=502, detail="ask-ai did not return valid JSON.")
