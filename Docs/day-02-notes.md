# Day 2 notes

## Prediction vs. reality
I predicted about 4 of the 14 checked models would work. 9 worked: all 4 Groq models and 5 of the first 10 Gemini models.

## What surprised me
A lot more models returned ok than expected.

| provider | model | status | latency |
|---|---|---|---|
| groq | allam-2-7b | ok | 0.20s |
| groq | openai/gpt-oss-120b | ok | 0.61s |
| groq | openai/gpt-oss-20b | ok | 0.47s |
| groq | qwen/qwen3.8-27b | ok | 0.15s |
| gemini | gemini-2.5-flash | not_found | 0.51s |
| gemini | gemini-2.5-flash-lite | not_found | 0.39s |
| gemini | gemini-2.5-pro | not_found | 0.49s |
| gemini | gemini-3-flash-preview | ok | 2.37s |
| gemini | gemini-3.1-flash-lite | ok | 12.51s |
| gemini | gemini-3.1-flash-lite-preview | ok | 4.53s |
| gemini | gemini-3.1-pro-preview | rate_limit | 0.43s |
| gemini | gemini-3.1-pro-preview-customtools | rate_limit | 0.41s |
| gemini | gemini-3.5-flash | ok | 7.85s |
| gemini | gemini-3.5-flash-lite | ok | 6.17s |

## Error types I saw
- `not_found` means the model is gone (for my account: it's still in the list).
- `rate_limit` means slow down.

## Open question
Why did the pro models hit rate limit instantly?

What I learned: Gemini's full message said `limit: 0` for free-tier requests to `gemini-3.1-pro`. The free tier allows zero messages to pro models, so it's not "slow down", it's "not on your plan". The same `rate_limit` sticker hides two situations: busy (try later) and never allowed (stop trying).
