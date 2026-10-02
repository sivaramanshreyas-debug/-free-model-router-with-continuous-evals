"""The adapter: one way to talk to every provider.

The rest of the app only ever calls list_models() and ask(). It never needs to know
which company is on the other end. That's what lets the router swap models freely.
"""

import os
import time
from dataclasses import dataclass

import openai
from dotenv import load_dotenv
from openai import OpenAI

from providers import PROVIDERS

load_dotenv()  # reads your keys from the .env file

TIMEOUT_S = 60


class MissingKeyError(RuntimeError):
    pass


@dataclass
class Result:
    provider: str
    model: str
    text: str | None
    latency_s: float               # how long the call took, in seconds
    input_tokens: int | None       # size of what we sent
    output_tokens: int | None      # size of what came back
    error: str | None = None       # filled in if the call failed (e.g. rate limit)
    error_type: str | None = None  # rate_limit | auth | not_found | timeout | connection | other


def client_for(provider: str) -> OpenAI:
    cfg = PROVIDERS[provider]
    key = os.getenv(cfg["api_key_env"])
    if not key:
        raise MissingKeyError(f"Missing {cfg['api_key_env']} in your .env file")
    # No hidden retries: the router decides what to do after a failure.
    return OpenAI(base_url=cfg["base_url"], api_key=key, timeout=TIMEOUT_S, max_retries=0)


def classify_error(e: Exception) -> str:
    # Timeout must be checked before connection: APITimeoutError is a subclass of APIConnectionError.
    if isinstance(e, openai.APITimeoutError):
        return "timeout"
    if isinstance(e, openai.APIConnectionError):
        return "connection"
    if isinstance(e, openai.RateLimitError):
        return "rate_limit"
    if isinstance(e, (openai.AuthenticationError, openai.PermissionDeniedError, MissingKeyError)):
        return "auth"
    if isinstance(e, openai.NotFoundError):
        return "not_found"
    return "other"


def list_models(provider: str) -> list[str]:
    """Ask the provider which models it offers right now."""
    models = client_for(provider).models.list()
    return sorted(m.id.removeprefix("models/") for m in models)


def ask(provider: str, model: str, prompt: str) -> Result:
    """Send one prompt to one model. Never crashes: failures come back as a Result with an error."""
    start = time.perf_counter()
    try:
        resp = client_for(provider).chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        usage = resp.usage
        return Result(
            provider=provider,
            model=model,
            text=resp.choices[0].message.content,
            latency_s=time.perf_counter() - start,
            input_tokens=usage.prompt_tokens if usage else None,
            output_tokens=usage.completion_tokens if usage else None,
        )
    except Exception as e:
        return Result(
            provider, model, None, time.perf_counter() - start, None, None,
            error=str(e), error_type=classify_error(e),
        )
