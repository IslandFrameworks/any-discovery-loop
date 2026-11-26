#!/usr/bin/env python3
"""Integrate step: append a round's section.md to Volume VI with an execution table generated from the actual results
file, plus Claude's verdict notes (loop/rounds/NNN/claude_check.md, written by Claude after running the checks).

    python3 loop/integrate.py N

Refuses to integrate if the results file is missing, if any recorded Z3 outcome differs from its expectation, or if
claude_check.md contains the word REJECT. Nothing else is edited; PROGRESS/OPEN/ANY navigation stay with Claude.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOLUME = os.path.join(ROOT, "volumes", "11_Laws_Research_Volume_VI.md")


def main():
    n = int(sys.argv[1])
    rd = os.path.join(ROOT, "loop", "rounds", f"{n:03d}")
    meta = json.load(open(os.path.join(rd, "meta.json")))
    sec, topic = meta["section"], meta["topic"]
    data_path = os.path.join(ROOT, "graph", "data", f"s{sec}_{topic}.json")
    if not os.path.exists(data_path):
        sys.exit(f"no results file {data_path}; run python -m graph.derive_{topic}_s{sec} first")
    data = json.load(open(data_path))
    bad = [r["name"] for r in data["z3"] if r["result"] != r["expected"]]
    if bad:
        sys.exit(f"Z3 outcomes differ from expectation: {bad}")
    check = open(os.path.join(rd, "claude_check.md"), encoding="utf-8").read()
    if re.search(r"\bREJECT\b", check):
        sys.exit("claude_check.md marks this round REJECT; not integrating")
    section = open(os.path.join(rd, "section.md"), encoding="utf-8").read().rstrip()
    if f"## §{sec}" in open(VOLUME, encoding="utf-8").read():
        sys.exit(f"§{sec} already in the volume")
    rows = "\n".join(f"| `{r['name']}` | {r['result'].upper()} | {r['expected'].upper()} |" for r in data["z3"])
    notes = "\n".join(l for l in check.splitlines()[1:] if l.strip())
    record = f"""

### {sec}.X Execution record (Claude; table generated from `graph/data/s{sec}_{topic}.json`)

`python -m graph.derive_{topic}_s{sec}` ran **{len(data['z3'])} Z3 queries**, every outcome matching its expectation,
plus the SymPy checks recorded in the data file; `graph/tests/test_{topic}_s{sec}.py` replays them. Checks written by
the loop's implement step ({meta.get('implementer', 'argon')}); run and judged by Claude.

| Query | Result | Expected |
|---|---|---|
{rows}

**Claude's verdicts:**
{notes}
"""
    with open(VOLUME, "a", encoding="utf-8") as f:
        f.write("\n\n" + section + record)
    print(f"§{sec} appended ({len(section) + len(record)} chars)")


if __name__ == "__main__":
    main()
