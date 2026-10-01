"""The provider registry: a list of every free model provider the router knows about.

Each entry says where the provider lives (base_url) and which secret key it needs.
Adding a provider later = adding one entry here. Nothing else should need to change.
"""

PROVIDERS = {
    "gemini": {
        # Google's OpenAI-compatible endpoint for the Gemini API
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "api_key_env": "GEMINI_API_KEY",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
    },
}
