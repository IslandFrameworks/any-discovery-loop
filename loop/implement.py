#!/usr/bin/env python3
"""Implement step: a model (Argon by default, GPT-6 via Codex with --gpt) turns a finished round's revised section and
claims into the archive's executable form, so Claude only runs, reads and judges.

    python3 loop/implement.py N [--gpt | --agy] [--topic short_name]

Writes graph/derive_<topic>_s<SEC>.py, graph/tests/test_<topic>_s<SEC>.py and loop/rounds/NNN/section.md (the volume
section text without rebuttals or claims JSON). Nothing is run and the volume is not touched; see loop/integrate.py.
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import discover  # reuses the Argon / GPT callers, ledger and paths

ROOT, LOOP = discover.ROOT, discover.LOOP

TEMPLATE = os.path.join(ROOT, "graph", "derive_anatomy_of_two_s482.py")
TEST_TEMPLATE = os.path.join(ROOT, "graph", "tests", "test_anatomy_of_two_s482.py")

BRIEF = """You are the IMPLEMENTER for a finished research round on Graham's ANY framework. Turn the revised Volume VI
section and its claims into executable checks in the archive's exact convention, so that Claude only has to run them.

Write TWO files, each introduced by a line `=== FILE: <relative path> ===` and then the full file content (no code
fences inside the file block). Paths:
  graph/derive_{topic}_s{sec}.py   graph/tests/test_{topic}_s{sec}.py
Keep both files compact (target under 600 lines total); encode each claim once, no long comments.

Rules for the derive script (follow the template below exactly in structure):
- `solver_record(name, constraints, expected, witness_vars)` with a 15 s timeout; UNKNOWN must fail. If a Z3 query is
  nonlinear and may time out, certify that claim by exact SymPy in `symbolic_certificates()` instead and say so.
- Encode EVERY claim and every weight-bearing number in the section (determinants, coefficients, signs, limits,
  integrals). Compute them; do not restate them. Where the section states a value, assert the computed value against
  it so a wrong draft value FAILS loudly.
- `main()` writes graph/data/s{sec}_{topic}.json (z3 list + sympy dict + versions), `json.dumps(..., default=str)`.
- Module docstring: section number, provenance (loop/rounds/{nnn}), and the encoded-family scope note.
Rules for the test file: replay every serialized SMT query (`solver.from_string`) and add at least three independent
controls that recompute key results by a DIFFERENT method than the derive script (numeric vs symbolic, another form).
===== TEMPLATE derive script =====
{template}

===== TEMPLATE test file =====
{test_template}

===== REVISED SECTION (04_revise.md) =====
{revise}

===== CLAIMS (claims.json) =====
{claims}
"""


def parse_files(text):
    parts = re.split(r"^=== FILE: (.+?) ===\s*$", text, flags=re.M)
    files = {}
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1].strip("\n")
        body = re.sub(r"^```[a-z]*\n|\n```$", "", body)       # tolerate stray fences
        files[parts[i].strip()] = body.rstrip() + "\n"
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("round", type=int)
    provider = ap.add_mutually_exclusive_group()
    provider.add_argument("--gpt", action="store_true", help="use your configured Codex CLI")
    provider.add_argument("--agy", action="store_true", help="use your configured Antigravity CLI")
    ap.add_argument("--argon", action="store_true", help="Argon instead of 3.8 Flash when GPT is not used")
    ap.add_argument("--topic", default="")
    a = ap.parse_args()
    discover.AGY = a.agy
    if a.gpt:
        discover.require_live_backend("codex")
    elif a.agy:
        discover.require_live_backend("agy")
    else:
        discover.vertex_spend_state()
    if a.argon:
        discover.MODEL = discover.ARGON
    rd = os.path.join(LOOP, "rounds", f"{a.round:03d}")
    meta = json.load(open(os.path.join(rd, "meta.json")))
    sec = meta["section"]
    revise = open(os.path.join(rd, "04_revise.md"), encoding="utf-8").read()
    topic = a.topic or re.sub(r"[^a-z0-9]+", "_", re.sub(r"\$.*?\$", "", revise.splitlines()[0].split("—", 1)[-1])
                               .lower()).strip("_")[:40] or f"round{a.round:03d}"
    prompt = BRIEF.format(topic=topic, sec=sec, nnn=f"{a.round:03d}", template=open(TEMPLATE).read(),
                          test_template=open(TEST_TEMPLATE).read(), revise=revise,
                          claims=open(os.path.join(rd, "claims.json"), encoding="utf-8").read())
    if a.gpt:
        text = discover.gpt(prompt, a.round, "implement")
        if not text:
            sys.exit("Codex returned no implementation.")
        implementer = "gpt"
    else:
        text = discover.argon(prompt, a.round, "implement", temperature=0.2, max_tokens=65000)
        implementer = "agy" if a.agy else "argon"
    open(os.path.join(rd, "05_implement_raw.md"), "w", encoding="utf-8").write(text)
    files = parse_files(text)
    allowed = {f"graph/derive_{topic}_s{sec}.py", f"graph/tests/test_{topic}_s{sec}.py"}
    written = []
    for path, body in files.items():
        if path not in allowed:
            print(f"skipped unexpected path {path}")
            continue
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w", encoding="utf-8").write(body)
        written.append(path)
    meta.update(implementer=implementer, topic=topic, implemented=written)
    json.dump(meta, open(os.path.join(rd, "meta.json"), "w"), indent=2)
    print("wrote:", *written, sep="\n  ")
    last = json.loads(open(os.path.join(LOOP, "ledger.jsonl")).read().splitlines()[-1])
    if last.get("finish") not in (None, "STOP"):
        sys.exit("implementer output truncated (MAX_TOKENS); files are incomplete")
    # section.md is mechanical: the revised draft minus rebuttals and the claims JSON
    sec_txt = re.split(r"\n-{3,}\s*\n+#{2,3} Rebuttals|\n#{2,3} Rebuttals", revise)[0].rstrip().rstrip("-").rstrip()
    sec_txt = re.sub(r"```json.*?```", "", sec_txt, flags=re.S).rstrip()
    m_sec = re.search(rf"^## §{sec}\b", sec_txt, re.M)
    if m_sec:
        sec_txt = sec_txt[m_sec.start():]   # drop any developer preamble above the section heading
    open(os.path.join(rd, "section.md"), "w", encoding="utf-8").write(sec_txt + "\n")
    written.append(f"loop/rounds/{a.round:03d}/section.md")
    meta["implemented"] = written
    json.dump(meta, open(os.path.join(rd, "meta.json"), "w"), indent=2)
    if len(written) < 3:
        sys.exit("implement step incomplete; see 05_implement_raw.md")


if __name__ == "__main__":
    main()
