"""Health check: find out which chat models actually work right now."""

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
