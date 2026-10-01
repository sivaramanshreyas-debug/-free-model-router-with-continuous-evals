# free-router

A router that sends each task to the best currently available **free** AI model,
shows why it chose that model, and keeps its choices honest with its own scheduled
evals.

## Day 1

- `providers.py` — registry of free providers (Gemini, Groq)
- `adapter.py` — `list_models()` and `ask()`, the only code that talks to providers
- `day1.py` — command-line script to list models and compare two providers on one prompt

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env and add your Gemini and Groq API keys
python day1.py list
python day1.py ask gemini:<model-id> groq:<model-id>
```

## Status

- [ ] Day 1: provider registry, adapter, model listing
