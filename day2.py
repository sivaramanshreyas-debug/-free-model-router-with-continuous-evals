"""Day 2: find out which free chat models actually work right now.

Usage:
  python day2.py check                      (all providers)
  python day2.py check groq
  python day2.py check gemini --limit 10
"""

import sys

from day1 import log_result, print_table
from health import HEALTH_PATH, PROBE_PROMPT, check_provider, save_health
from providers import PROVIDERS


def cmd_check(args):
    limit = None
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])
        args = [a for a in args if a not in ("--limit", str(limit))]
    providers = args or list(PROVIDERS)

    for provider in providers:
        print(f"\n== Checking {provider} (1 second pause between models) ==")
        try:
            results = check_provider(provider, limit=limit)
        except Exception as e:
            print(f"   could not list models: {type(e).__name__}")
            continue
        for r in results:
            log_result(r, PROBE_PROMPT)
        print_table(results)
        save_health(provider, results)
        working = sum(1 for r in results if not r.error_type)
        print(f"{working} of {len(results)} working. Snapshot saved to {HEALTH_PATH}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "check":
        cmd_check(sys.argv[2:])
    else:
        print(__doc__)
