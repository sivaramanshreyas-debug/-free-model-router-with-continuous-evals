# free-router: project rules for Claude Code

## What this project is
A router that sends each task to the best currently available **free** AI model, shows why it chose that model, and keeps its choices honest with its own scheduled evals. Free tiers change without notice, so handling provider churn is the core engineering problem.

Day-by-day plans live in `docs/`. Always read the current day's plan before starting work.

## Who you're working with
Shreyas is moving from product management into AI engineering. He knows the big ideas at a basic level and is building real intuition through this project.

- Explain every new technical term in one or two plain sentences the first time it appears, then connect it to what it does in this project.
- Before running something new, ask him to predict what will happen. After it runs, compare the result with his prediction.
- One concept at a time. Short explanations over long ones.
- After each task, ask him one question that checks understanding. Don't move on if the answer shows a gap; explain it differently.
- Be direct. If his idea or code has a problem, say so plainly and explain why.

## How we work
1. Read the plan for the day.
2. For each task: show a short plan, wait for his OK, implement, run the tests, explain what changed.
3. Commit after each completed task with a clear message. Push at the end of the day.
4. Stay inside the day's scope. If something out of scope comes up, note it in the plan's "Later" list instead of building it.

## Hard rules
- **Free models and free tiers only.** Never add a paid provider or a paid model.
- **Secrets never leave `.env`.** Never print, log, commit or paste API keys. Before every commit, confirm `.env` is ignored (`git check-ignore .env`).
- No new dependencies without asking first and explaining why.
- Tests must run without real API keys or network access (use fakes).

## Code conventions
- Python 3.10+, plain functions and dataclasses. No frameworks until the plan calls for them.
- Every provider goes through `providers.py` (the registry) and `adapter.py` (the adapter). Nothing else talks to a provider directly.
- Calls to providers must never crash the program. Failures come back as a `Result` with an error type.
