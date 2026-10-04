"""judge_efficiency.py — measured per-item latency and token usage for judge runs.

Reads judge outputs that carry the telemetry fields added 2026-10-04:
  mqm_judge.py  latency_s (wall-clock incl. retries), attempts, usage = Gemini usageMetadata
                (promptTokenCount, candidatesTokenCount, thoughtsTokenCount, totalTokenCount)
  jev_judge.py  latency_s (API call), usage = {input_tokens, output_tokens}
Reports tokens, not money: no price list is assumed. Latency is wall-clock from this machine and
includes network time, so it is indicative of the user experience, not of server compute.

Usage:
    python judge_efficiency.py --judge gemini:.../gemini_on_v3_run2.jsonl --judge jev:.../jev_on_v3_run2.jsonl
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def tokens(u: dict | None) -> dict:
    if not u:
        return {}
    if "input_tokens" in u:  # JEV
        return {"input": u.get("input_tokens", 0), "output": u.get("output_tokens", 0), "thinking": 0}
    return {"input": u.get("promptTokenCount", 0), "output": u.get("candidatesTokenCount", 0),
            "thinking": u.get("thoughtsTokenCount", 0)}


def q(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--judge", action="append", required=True, help="label:path")
    args = ap.parse_args(argv)
    print(f"{'judge':<16}{'n':>5}{'lat mean':>10}{'median':>8}{'p90':>8}{'total s':>9}"
          f"{'in tok':>9}{'out tok':>9}{'think tok':>10}{'total tok':>10}{'retries':>9}")
    for spec in args.judge:
        label, path = spec.split(":", 1)
        rs = [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
        rs = [r for r in rs if r.get("latency_s") is not None]
        if not rs:
            print(f"{label:<16} no telemetry")
            continue
        lat = [r["latency_s"] for r in rs]
        tk = [tokens(r.get("usage")) for r in rs]
        tk = [t for t in tk if t]
        mean = lambda k: st.mean(t[k] for t in tk) if tk else float("nan")  # noqa: E731
        tot = [t["input"] + t["output"] + t["thinking"] for t in tk]
        retries = sum(max(0, (r.get("attempts") or 1) - 1) for r in rs)
        print(f"{label:<16}{len(rs):>5}{st.mean(lat):>10.2f}{st.median(lat):>8.2f}{q(lat, .9):>8.2f}{sum(lat):>9.0f}"
              f"{mean('input'):>9.0f}{mean('output'):>9.0f}{mean('thinking'):>10.0f}{(st.mean(tot) if tot else 0):>10.0f}{retries:>9}")
    print("\nPer-item means; 'total tok' = input + output + thinking. Gemini thinking tokens are billed as output by Google;"
          "\nJEV has no thinking tokens. Prices are not applied here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
