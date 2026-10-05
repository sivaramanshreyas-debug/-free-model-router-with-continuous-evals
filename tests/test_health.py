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
