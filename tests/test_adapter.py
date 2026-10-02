from types import SimpleNamespace

import httpx2
import openai

import adapter

REQ = httpx2.Request("POST", "https://example.test/chat/completions")


class FakeClient:
    """Stands in for the OpenAI client: returns a scripted reply or raises a scripted error."""

    def __init__(self, reply=None, error=None, model_ids=()):
        self._reply = reply
        self._error = error
        self.models = SimpleNamespace(list=lambda: [SimpleNamespace(id=m) for m in model_ids])
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        if self._error:
            raise self._error
        return self._reply


def use_fake(monkeypatch, client):
    monkeypatch.setattr(adapter, "client_for", lambda provider: client)


def fake_reply(text, prompt_tokens, completion_tokens):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=text))],
        usage=SimpleNamespace(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens),
    )


def test_list_models_strips_prefix_and_sorts(monkeypatch):
    use_fake(monkeypatch, FakeClient(model_ids=["models/gemini-b", "models/gemini-a", "llama-3"]))

    assert adapter.list_models("gemini") == ["gemini-a", "gemini-b", "llama-3"]


def test_ask_success_returns_text_latency_and_tokens(monkeypatch):
    use_fake(monkeypatch, FakeClient(reply=fake_reply("Hello!", 12, 3)))

    r = adapter.ask("groq", "some-model", "hi")

    assert r.text == "Hello!"
    assert r.input_tokens == 12
    assert r.output_tokens == 3
    assert r.latency_s >= 0
    assert r.error is None
    assert r.error_type is None


def test_ask_rate_limit_is_classified(monkeypatch):
    err = openai.RateLimitError("slow down", response=httpx2.Response(429, request=REQ), body=None)
    use_fake(monkeypatch, FakeClient(error=err))

    r = adapter.ask("groq", "some-model", "hi")

    assert r.text is None
    assert r.error_type == "rate_limit"


def test_ask_timeout_is_classified(monkeypatch):
    use_fake(monkeypatch, FakeClient(error=openai.APITimeoutError(request=REQ)))

    r = adapter.ask("gemini", "some-model", "hi")

    assert r.text is None
    assert r.error_type == "timeout"
