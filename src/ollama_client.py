from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any
from urllib import error, request


class OllamaError(RuntimeError):
    """Raised when the local Ollama API cannot complete a requested operation."""


class OllamaClient:
    def __init__(self, base_url: str, timeout: int = 300) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def chat(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        image_paths: list[Path] | None = None,
        temperature: float = 0.2,
    ) -> str:
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        if image_paths:
            messages[-1]["images"] = [self._encode_image(path) for path in image_paths]

        body = json.dumps(
            {
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature},
            },
        ).encode("utf-8")

        http_request = request.Request(
            f"{self.base_url}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(http_request, timeout=self.timeout) as response:
                response_text = response.read().decode("utf-8")
        except error.HTTPError as exc:
            response_text = exc.read().decode("utf-8", errors="replace")
            raise OllamaError(
                f"Ollama API request failed with status {exc.code}: {response_text[:500]}"
            ) from exc
        except error.URLError as exc:
            raise OllamaError(f"Could not connect to Ollama at {self.base_url}: {exc}") from exc

        payload = json.loads(response_text)
        message = payload.get("message")
        if not isinstance(message, dict) or not isinstance(message.get("content"), str):
            raise OllamaError("Ollama response does not contain message.content.")
        return message["content"].strip()

    def generate(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:
        prompt = f"{system_prompt.strip()}\n\nUSER INPUT:\n{user_prompt.strip()}"
        body = json.dumps(
            {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature},
            },
        ).encode("utf-8")

        http_request = request.Request(
            f"{self.base_url}/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(http_request, timeout=self.timeout) as response:
                response_text = response.read().decode("utf-8")
        except error.HTTPError as exc:
            response_text = exc.read().decode("utf-8", errors="replace")
            raise OllamaError(
                f"Ollama generate request failed with status {exc.code}: {response_text[:500]}"
            ) from exc
        except error.URLError as exc:
            raise OllamaError(f"Could not connect to Ollama at {self.base_url}: {exc}") from exc

        payload = json.loads(response_text)
        content = payload.get("response")
        if not isinstance(content, str):
            raise OllamaError("Ollama generate response does not contain response text.")
        return content.strip()

    @staticmethod
    def _encode_image(path: Path) -> str:
        if not path.exists():
            raise FileNotFoundError(f"Image file does not exist: {path}")
        return base64.b64encode(path.read_bytes()).decode("ascii")
