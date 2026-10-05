"""Health check: find out which chat models actually work right now."""

import time

from adapter import Result, ask, list_models

PROBE_PROMPT = "Reply with the word OK."

# A model whose name contains any of these words can't do text chat.
NON_CHAT_WORDS = (
    "image", "tts", "embedding", "veo", "lyria", "whisper", "transcribe",
    "guard", "live", "audio", "robotics", "orpheus", "nano-banana",
    "deep-research", "computer-use", "antigravity", "aqa",
)


def is_chat_candidate(model_id: str) -> bool:
    """The bouncer: True if the name doesn't contain any non-chat word."""
    name = model_id.lower()
    return not any(word in name for word in NON_CHAT_WORDS)


def probe(provider: str, model: str) -> Result:
    """Knock on one door: send a tiny prompt and see what comes back."""
    return ask(provider, model, PROBE_PROMPT)


def check_provider(provider: str, limit: int | None = None, pause_s: float = 1.0) -> list[Result]:
    """Probe every chat model a provider lists, pausing between calls to protect the free quota."""
    candidates = [m for m in list_models(provider) if is_chat_candidate(m)]
    if limit is not None:
        candidates = candidates[:limit]

    results = []
    for i, model in enumerate(candidates):
        if i > 0:
            time.sleep(pause_s)
        results.append(probe(provider, model))
    return results
