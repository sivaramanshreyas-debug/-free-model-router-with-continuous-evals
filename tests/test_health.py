import health
from adapter import Result
from health import is_chat_candidate

# Real names from the Day 1 `list` output.
CHAT_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest",
    "gemma-4-31b-it",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "allam-2-7b",
]

NOT_CHAT_MODELS = [
    "gemini-2.5-flash-image",
    "gemini-2.5-flash-preview-tts",
    "gemini-embedding-001",
    "veo-3.1-generate-preview",
    "lyria-3.5",
    "whisper-large-v3",
    "meta-llama/llama-prompt-guard-2-22m",
    "openai/gpt-oss-safeguard-20b",
    "canopylabs/orpheus-v1-english",
    "gemini-3.8-live",
    "gemini-3.5-transcribe",
    "gemini-robotics-er-2-preview",
    "nano-banana-pro-preview",
    "deep-research-preview-04-2026",
    "gemini-2.5-computer-use-preview-10-2025",
    "antigravity-preview-latest",
    "aqa",
]


def test_bouncer_lets_chat_models_in():
    for name in CHAT_MODELS:
        assert is_chat_candidate(name), name


def test_bouncer_keeps_other_models_out():
    for name in NOT_CHAT_MODELS:
        assert not is_chat_candidate(name), name


def use_fakes(monkeypatch, listed):
    """Fake list_models() and ask(); return the list of models that got a probe."""
    probed = []

    def fake_ask(provider, model, prompt):
        probed.append(model)
        return Result(provider, model, "OK", 0.1, 5, 1)

    monkeypatch.setattr(health, "list_models", lambda provider: listed)
    monkeypatch.setattr(health, "ask", fake_ask)
    return probed


def test_check_provider_only_probes_chat_models(monkeypatch):
    probed = use_fakes(monkeypatch, ["gemini-3.5-flash", "veo-3.1-generate-preview", "gemma-4-31b-it"])

    results = health.check_provider("gemini", pause_s=0)

    assert probed == ["gemini-3.5-flash", "gemma-4-31b-it"]
    assert [r.model for r in results] == probed


def test_check_provider_respects_limit(monkeypatch):
    probed = use_fakes(monkeypatch, ["a-chat", "b-chat", "c-chat", "d-chat"])

    results = health.check_provider("groq", limit=2, pause_s=0)

    assert probed == ["a-chat", "b-chat"]
    assert len(results) == 2
