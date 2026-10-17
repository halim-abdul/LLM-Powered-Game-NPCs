"""Dependency-free providers; credentials stay outside source control."""
import json
import os
import urllib.request
from urllib.parse import urlparse


class OfflineProvider:
    """Deterministic fixture for integration tests, not an LLM."""
    def generate(self, system, context):
        lore = context["lore"]
        detail = lore[0]["text"] if lore else "I have no reliable information about that."
        return {"dialogue": f'{context["character"]["name"]}: {detail}', "action": "talk"}


class HTTPProvider:
    """Adapter for a configured OpenAI-compatible chat completions endpoint."""
    def __init__(self, endpoint, model, api_key=None, timeout=20):
        parsed = urlparse(endpoint)
        if parsed.scheme != "https" and not (
            parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}
        ):
            raise ValueError("Use HTTPS or a loopback HTTP endpoint")
        self.endpoint, self.model = endpoint, model
        self.api_key = api_key if api_key is not None else os.getenv("NPC_API_KEY", "")
        self.timeout = timeout

    def generate(self, system, context):
        body = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(context)},
            ],
            "temperature": 0.5,
        }).encode()
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = urllib.request.Request(self.endpoint, data=body, headers=headers)
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            payload = json.loads(response.read(1_000_000))
        return json.loads(payload["choices"][0]["message"]["content"])
