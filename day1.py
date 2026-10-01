"""Day 1: see what's available, then race two models on the same question.

Usage:
  python day1.py list
  python day1.py ask gemini:<model-id> groq:<model-id>
"""

import sys

from adapter import ask, list_models
from providers import PROVIDERS

PROMPT = "Explain what an API rate limit is in two sentences, for a beginner."


def cmd_list():
    for provider in PROVIDERS:
        print(f"\n== {provider} ==")
        try:
            for model in list_models(provider):
                print("  ", model)
        except Exception as e:
            print("   could not list models:", e)


def cmd_ask(targets):
    print(f"Prompt: {PROMPT}\n")
    for target in targets:
        provider, model = target.split(":", 1)
        r = ask(provider, model, PROMPT)
        print(f"--- {r.provider} / {r.model} ---")
        print(f"latency: {r.latency_s:.2f}s | tokens in: {r.input_tokens} | tokens out: {r.output_tokens}")
        print(f"ERROR: {r.error}\n" if r.error else f"{r.text}\n")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "list":
        cmd_list()
    elif len(sys.argv) >= 3 and sys.argv[1] == "ask":
        cmd_ask(sys.argv[2:])
    else:
        print(__doc__)
