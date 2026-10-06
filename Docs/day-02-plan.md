# Day 2: health check — which free models actually work right now

## Goal in plain terms
Day 1 proved that "listed" does not mean "usable": `gemini-2.5-flash` was listed but returned 404, and `gemini-3.8-flash` was overloaded three times in a row. Today we build a health check that tries each chat model with a tiny prompt and saves which ones work for this account. The router (coming soon) will only ever pick from models the health check says are working.

## Starting point
| File | Role |
|---|---|
| `providers.py` | Registry, with `validate_registry()` |
| `adapter.py` | `list_models()` and `ask()`, with a timeout and classified errors |
| `day1.py` | `list` and `ask`, logging to `results/runs.jsonl` |
| `tests/` | 6 offline tests |
| `Docs/day-01-plan.md` | "Later" list: today picks up the first three items |

## In scope
Gemini and Groq only, text chat only, command line only. A new `health.py` module and a `day2.py check` command.

## Out of scope (do not build today)
Choosing between models (routing), judging answer quality (evals), running checks on a schedule, a third provider, a web UI. Add ideas to the "Later" list at the bottom.

---

## Task 1: Start-of-day check
**Do:**
- Confirm `pytest` still passes and `git check-ignore .env` still reports it ignored.
- If the API keys pasted into chat on Day 1 haven't been replaced yet, regenerate both and update `.env` by hand in a text editor.

**Done when:** tests pass, `.env` is ignored, and the keys in `.env` have never appeared in a chat.

**Learning checkpoint:** key rotation; why a secret that has been seen anywhere outside `.env` counts as leaked.

## Task 2: A label for "server overloaded"
**Do:**
- Add an `unavailable` error type to `classify_error()` for `openai.InternalServerError` (the library raises it for every 5xx status, including Day 1's 503).
- Add a test that a 503 is classified as `unavailable`.

**Done when:** a fake 503 comes back as `unavailable` and all tests pass.

**Learning checkpoint:** 4xx vs 5xx status codes ("you did something wrong" vs "the server has a problem"). Why `unavailable` and `rate_limit` lead to the same router action (try another model) but `other` doesn't.

## Task 3: Keep only chat models
**Do:**
- In a new `health.py`, add `is_chat_candidate(model_id) -> bool` that rejects names containing words like `tts`, `embedding`, `image`, `veo`, `lyria`, `whisper`, `transcribe`, `guard`, `live`, `audio`, `robotics`.
- Test it against real names from Day 1's `list` output (kept and rejected).

**Done when:** running the filter over Day 1's list keeps only text chat models, and the tests pass.

**Learning checkpoint:** heuristic. Why filtering by name is quick but fragile, and why that's exactly why Task 4 actually tries each model instead of trusting names.

## Task 4: Probe each model
**Do:**
- Add `probe(provider, model) -> Result` in `health.py`: sends a tiny prompt ("Reply with the word OK.") through `ask()`. No direct provider calls: everything still goes through the adapter.
- Add `check_provider(provider, limit=None, pause_s=1.0)`: lists models, filters with `is_chat_candidate()`, probes each with a short pause between calls, and returns the results.

**Done when:** with a fake `ask()`, `check_provider()` probes only chat candidates, respects `limit`, and returns one result per model.

**Learning checkpoint:** quota (free tiers cap requests per minute and per day). Why we pause between calls and allow a `limit`: probing 40 models at full speed is a good way to rate-limit ourselves.

## Task 5: Save the health snapshot
**Do:**
- Add `day2.py check [provider] [--limit N]`: runs the check, prints a table (provider, model, status, latency), appends every probe to `results/runs.jsonl`, and writes `results/health.json` with each model's status, latency and `checked_at` time.
- Each run replaces its own provider's section of `health.json` (so checking Gemini doesn't erase Groq); `runs.jsonl` keeps growing.

**Done when:** running `check` twice leaves one up-to-date `health.json` and twice as many probe lines in `runs.jsonl`.

**Learning checkpoint:** snapshot vs. log. `health.json` answers "what works *now*"; `runs.jsonl` answers "what has happened *over time*". The router reads the first; evals and trends read the second.

## Task 6: Tests without network
**Do:**
- Tests for: `unavailable` classification, `is_chat_candidate()`, `check_provider()` with a fake `ask()` (filtering, `limit`, one result per model), and `health.json` being written in the right shape to a temporary folder.
- Run `pytest` with the network blocked.

**Done when:** all tests pass offline.

**Learning checkpoint:** temporary folders in tests (`tmp_path`), so tests never touch the real `results/`.

## Task 7: Run it for real
**Do:**
- Shreyas predicts: out of Gemini's chat candidates, how many will actually answer? Same for Groq.
- Run `python day2.py check groq`, then `python day2.py check gemini --limit 10`. Compare with the prediction.
- Write `Docs/day-02-notes.md` in Shreyas's own words: what worked, what didn't, which error types appeared, anything surprising.

**Done when:** `health.json` lists real results for both providers and the notes are written.

**Learning checkpoint:** provider churn. Running the same check tomorrow may give a different answer, and that's the whole reason the project needs scheduled checks later.

## Task 8: Wrap up
**Do:**
- Tick the Day 1 "Later" items handled today, update the README status, confirm `.env` is ignored and no keys are in git history, commit and push.

**Done when:** GitHub shows today's work, tests pass, and no secrets are in the repo.

---

## Definition of done for Day 2
- [x] Keys rotated; `.env` still ignored; no keys in git history
- [x] 5xx errors labelled `unavailable`
- [x] `is_chat_candidate()` filters out non-chat models
- [x] `check_provider()` probes chat models politely (pause + limit)
- [x] `results/health.json` holds the latest status of every probed model
- [x] `pytest` passes without network
- [x] Real health check run on both providers
- [x] `Docs/day-02-notes.md` written by Shreyas
- [x] README updated, committed, pushed

## End-of-day quiz (Claude asks, Shreyas answers)
1. Why can't the router trust `list_models()` on its own?
2. What's the difference between a 4xx and a 5xx error, and which one is usually your fault?
3. Why does `health.json` get replaced each run while `runs.jsonl` keeps growing?
4. Why does the health check pause between calls?

## Later (parking lot)
- Token counts aren't comparable across models (`gpt-oss` adds hidden setup and reasoning tokens). Matters once we track free-tier usage. *(carried over from Day 1)*
- Split `rate_limit` in two: "busy, try later" vs "not on your plan". Gemini's `pro` models return 429 with `limit: 0` on the free tier, which will never work; the router should stop trying them instead of retrying later.
- `list_models()` failing (e.g. a bad key) still raises; `day2.py` catches it. If the router needs it, return it as a labelled failure like `ask()` does.
