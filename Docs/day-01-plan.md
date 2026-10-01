# Day 1: provider registry, adapter, list models, compare two providers

## Goal in plain terms
Talk to two free AI providers from our own code, through one common doorway, and compare their answers side by side. Every later feature (evals, routing, the "why" card) sits on top of this.

## Starting point
These files already exist and form a working first draft:

| File | Role |
|---|---|
| `providers.py` | **Registry**: where each provider lives and which key it needs |
| `adapter.py` | **Adapter**: `list_models()` and `ask()`, the only code that talks to providers |
| `day1.py` | Command-line script: `list` and `ask` |
| `.env.example`, `.gitignore`, `requirements.txt`, `README.md` | Setup |

Today's job is to verify the draft, make it sturdier, add tests and a results log, and run it for real.

## In scope
Gemini and Groq only, text chat only, command line only.

## Out of scope (do not build today)
Evals, routing logic, a web UI, a third provider, images or audio. Add ideas to the "Later" list at the bottom.

---

## Task 1: Environment and secrets check
**Do:**
- Confirm Python is 3.10 or newer, create `.venv`, install `requirements.txt`.
- Confirm `.env` exists with both keys filled in (check presence only; never print the values).
- Confirm `git check-ignore .env` reports it as ignored.

**Done when:** dependencies install cleanly and `.env` is proven ignored.

**Learning checkpoint:** virtual environment, environment variable, why secrets stay out of git.

## Task 2: Review the registry
**Do:**
- Walk Shreyas through `providers.py` entry by entry.
- Add a small `validate_registry()` check that every entry has `base_url` and `api_key_env`.

**Done when:** the registry validates and Shreyas can explain what adding a third provider would take.

**Learning checkpoint:** API, endpoint/base URL, API key, OpenAI-compatible.

## Task 3: Harden the adapter
**Do:**
- Add a request timeout (60 seconds) so a stuck provider can't hang the program.
- Add an `error_type` field to `Result` with one of: `rate_limit`, `auth`, `not_found`, `timeout`, `connection`, `other`. Map these from the `openai` library's exception classes.
- Keep the rule: `ask()` never raises; failures come back as a `Result`.

**Done when:** each failure type maps to the right `error_type`.

**Learning checkpoint:** exception, HTTP status codes (401, 404, 429), timeout. Why classifying errors matters later: a `rate_limit` means "try another model," but an `auth` error means "fix your key."

## Task 4: Tests without network
**Do:**
- Add `pytest` to `requirements.txt` (ask first, per project rules).
- Write tests in `tests/` using a fake client, so no keys or internet are needed:
  - registry validation passes and fails correctly
  - `list_models()` strips the `models/` prefix
  - `ask()` returns text, latency and token counts on success
  - `ask()` returns the correct `error_type` for a rate-limit error and a timeout
- Run `pytest` and get all tests passing.

**Done when:** `pytest` passes with the network turned off.

**Learning checkpoint:** unit test, fake/mock, why tests must not depend on a provider's mood that day.

## Task 5: Log every comparison
**Do:**
- Make `day1.py ask` append each result as one line of JSON to `results/runs.jsonl` (timestamp, provider, model, prompt, latency, tokens, error_type, answer).
- Add `results/` to `.gitignore`.
- Print a compact comparison table in the terminal: provider, model, latency, tokens in/out, status.

**Done when:** running `ask` twice produces two lines per model in `runs.jsonl`.

**Learning checkpoint:** JSONL, why we log raw results. These logs become the first data the observatory and router will learn from.

## Task 6: Run it for real
**Do:**
- Shreyas predicts which provider will be faster, then runs `python day1.py list` and `python day1.py ask gemini:<model> groq:<model>`.
- Run `ask` three times and compare latency across runs.
- Help Shreyas write `docs/day-01-notes.md` in his own words: what he saw, which numbers surprised him, any errors hit.

**Done when:** real answers from both providers are logged and the notes are written.

**Learning checkpoint:** latency, tokens, rate limit (if a `429` appears, celebrate: the error handling just proved itself).

## Task 7: Wrap up
**Do:**
- Update the README status checklist.
- Confirm `.env` is still ignored, commit, and push.

**Done when:** GitHub shows today's work, tests pass, and no secrets are in the repo.

---

## Definition of done for Day 1
- [ ] `.env` proven ignored; no keys anywhere in git history
- [ ] Registry validates
- [ ] Adapter has a timeout and classified errors; never crashes
- [ ] `pytest` passes without network
- [ ] `results/runs.jsonl` logs every comparison
- [ ] Real comparison run between Gemini and Groq
- [ ] `docs/day-01-notes.md` written by Shreyas
- [ ] README updated, committed, pushed

## End-of-day quiz (Claude asks, Shreyas answers)
1. What is the difference between the registry and the adapter?
2. Why does `ask()` return errors instead of crashing?
3. A call comes back with `error_type: rate_limit`. What should the router eventually do?
4. Why must tests run without the internet?

## Later (parking lot)
- 
