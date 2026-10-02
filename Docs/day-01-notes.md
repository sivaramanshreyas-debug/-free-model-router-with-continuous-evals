# Day 1 notes

## Prediction vs. reality
I thought Google would be more reliable than Groq.

## What surprised me
Groq's response time. Groq being faster surprised me.

| model | run 1 | run 2 | run 3 |
|---|---|---|---|
| groq `openai/gpt-oss-20b` | 0.59s | 0.67s | 0.56s |
| gemini `gemini-3.1-flash-lite` | 1.82s | 1.22s | 1.13s |
| gemini `gemini-3.5-flash` | 14.62s | 17.12s | 15.62s |

## Errors I hit
Gemini gave me a 404 (model retired) and a 503 (overloaded). Both taught me to switch models and to expect real-time API failures.

- `gemini-2.5-flash` → 404 `not_found`: listed by the provider, but no longer available to new users
- `gemini-3.8-flash` → 503 three times in a row, labelled `other` by our code

## Open question
How is OpenAI connected to Gemini?

What I learned: they aren't. OpenAI's request format is a shared standard. The `openai` library just builds the request, and `base_url` decides which company receives it.
