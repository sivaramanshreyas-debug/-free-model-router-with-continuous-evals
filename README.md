# free-router

A router that sends each task to the best currently available **free** AI model,
shows why it chose that model, and keeps its choices honest with its own scheduled
evals.

## Day 1

- `providers.py` — registry of free providers (Gemini, Groq)
- `adapter.py` — `list_models()` and `ask()`, the only code that talks to providers
- `day1.py` — command-line script to list models and compare two providers on one prompt

## Day 2

- `health.py` — health check: filters out non-chat models, probes each chat model with a tiny prompt, saves the results
- `day2.py check` — runs the health check and writes `results/health.json` (what works right now)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env and add your Gemini and Groq API keys
python day1.py list
python day1.py ask gemini:<model-id> groq:<model-id>
python day2.py check groq
python day2.py check gemini --limit 10
python -m pytest   # runs offline: no keys or network needed
```

Every call is appended to `results/runs.jsonl`; `day2.py check` also updates `results/health.json`. Both stay out of git.

## Status

- [x] Day 1: provider registry, adapter (timeout + classified errors), offline tests, results log, first real Gemini vs Groq comparison
- [x] Day 2: `unavailable` label for 5xx errors, chat-model filter, health check with `results/health.json`, first real check (9 of 14 models working)
