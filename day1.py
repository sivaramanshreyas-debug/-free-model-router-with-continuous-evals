"""Day 1: see what's available, then race two models on the same question.

Usage:
  python day1.py list
  python day1.py ask gemini:<model-id> groq:<model-id>
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from adapter import Result, ask, list_models
from providers import PROVIDERS

PROMPT = "Explain what an API rate limit is in two sentences, for a beginner."
LOG_PATH = Path(__file__).parent / "results" / "runs.jsonl"


def log_result(r: Result, prompt: str) -> None:
    """Append one result as a JSON line. Error messages are left out: they can echo key fragments."""
    LOG_PATH.parent.mkdir(exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "provider": r.provider,
        "model": r.model,
        "prompt": prompt,
        "latency_s": round(r.latency_s, 3),
        "input_tokens": r.input_tokens,
        "output_tokens": r.output_tokens,
        "error_type": r.error_type,
        "answer": r.text,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def print_table(results: list[Result]) -> None:
    rows = [("provider", "model", "latency", "in", "out", "status")]
    for r in results:
        rows.append((
            r.provider,
            r.model,
            f"{r.latency_s:.2f}s",
            str(r.input_tokens if r.input_tokens is not None else "-"),
            str(r.output_tokens if r.output_tokens is not None else "-"),
            r.error_type or "ok",
        ))
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    right_aligned = {2, 3, 4}
    for row in rows:
        cells = [c.rjust(w) if i in right_aligned else c.ljust(w) for i, (c, w) in enumerate(zip(row, widths))]
        print("  ".join(cells))


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
    results = []
    for target in targets:
        provider, model = target.split(":", 1)
        r = ask(provider, model, PROMPT)
        log_result(r, PROMPT)
        results.append(r)
        print(f"--- {r.provider} / {r.model} ---")
        print(f"ERROR ({r.error_type}): {r.error}\n" if r.error else f"{r.text}\n")
    print_table(results)
    print(f"\nLogged {len(results)} result(s) to {LOG_PATH}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "list":
        cmd_list()
    elif len(sys.argv) >= 3 and sys.argv[1] == "ask":
        cmd_ask(sys.argv[2:])
    else:
        print(__doc__)
