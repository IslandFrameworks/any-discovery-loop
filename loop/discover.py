#!/usr/bin/env python3
"""Discovery loop: Argon (Gemini 4, Vertex) and GPT-6 (Codex, when quota allows) take one research round to a
drafted Volume VI section plus testable claims. Claude then encodes and runs the claims, integrates the section and
commits; the next round reads Claude's verdicts. Nothing here edits the volumes or the registry.

    python3 loop/discover.py [--round N] [--no-gpt] [--argon] [--focus "question"] [--debate N]
(3.8 Flash by default; --argon for the strong model. Every Vertex call is checked against loop/spend.json.)

Round N writes loop/rounds/NNN/: 01_propose.md, 02_develop.md, 03_audit.md, 04_revise.md, claims.json, meta.json.
Turn order: propose (Argon) -> develop (Argon) -> adversarial audit (GPT-6 when Codex quota allows, else Argon)
-> revise (Argon). One GPT call per round keeps Codex usage low (Graham, 2026-10-13).
Context for every turn: ANY.md, active Volume VI (tail-capped), PROGRESS.md tail, loop/OPEN.md, and the previous
round's loop/rounds/<N-1>/claude_check.md. Every call is logged to loop/ledger.jsonl (tokens, served model, seconds).
"""
import argparse, datetime, json, os, re, subprocess, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOOP = os.path.join(ROOT, "loop")
VOLUME = os.path.join(ROOT, "volumes", "11_Laws_Research_Volume_VI.md")
PROJECT = os.environ.get("ANY_VERTEX_PROJECT", "")
ARGON = "gemini-4-argon"
FLASH = "gemini-3.8-flash"
MODEL = FLASH  # Graham 2026-10-14: Flash by default until the startup grant lands; Argon only with --argon
# Spend cap (Graham 2026-10-14: "it NEEDS to cut off"). Prices per 1M tokens, the HIGHER published rate
# (Argon $4/$20 after its $2/$10 promo; Flash $0.75/$3.75), thinking counted as output, so the estimate runs high.
PRICES = {ARGON: (4.0, 20.0), FLASH: (0.75, 3.75)}
# Context cache: cached input billed at 10% of input (published discount is larger), storage per 1M tokens per hour
# priced high; the whole TTL is charged up front when the cache is created.
CACHED_FRACTION = 0.10
STORAGE_PER_MTOK_HOUR = {ARGON: 4.5, FLASH: 1.0}
CACHE_TTL_S = 3600
CACHE = {}  # {"text": shared context, "name": cachedContents resource, "model": model}
SPEND_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spend.json")
SPEND_CAP = 60.0


def spend_state():
    try:
        return json.load(open(SPEND_FILE))
    except FileNotFoundError:
        return {"cap_usd": SPEND_CAP, "spent_usd": 0.0}


def vertex_disabled():
    """Graham's kill switch: "vertex_disabled": true in loop/spend.json blocks every Vertex call (credit exhausted)."""
    return bool(spend_state().get("vertex_disabled"))


def charge(model, prompt_tokens, output_tokens, cached_tokens=0, extra_usd=0.0):
    pin, pout = PRICES.get(model, PRICES[ARGON])
    fresh = (prompt_tokens or 0) - (cached_tokens or 0)
    st = spend_state()
    st["spent_usd"] = round(st["spent_usd"] + fresh / 1e6 * pin + (cached_tokens or 0) / 1e6 * pin * CACHED_FRACTION
                            + (output_tokens or 0) / 1e6 * pout + extra_usd, 4)
    json.dump(st, open(SPEND_FILE, "w"), indent=1)
    return st["spent_usd"]


def check_budget(model, prompt, max_tokens):
    """Refuse a call whose worst case (prompt ~ chars/3 tokens, full max_tokens out) would cross the cap."""
    pin, pout = PRICES.get(model, PRICES[ARGON])
    st = spend_state()
    worst = len(prompt) / 3 / 1e6 * pin + max_tokens / 1e6 * pout
    if st["spent_usd"] + worst > st["cap_usd"]:
        raise SystemExit(f"SPEND CAP: estimated ${st['spent_usd']:.2f} spent + ${worst:.2f} worst case for this call "
                         f"> cap ${st['cap_usd']:.2f} (loop/spend.json). Vertex call refused.")
GCLOUD = os.environ.get("ANY_GCLOUD", "gcloud")
CODEX = os.environ.get("ANY_CODEX", "codex")
AGY = None  # set by --agy: route Gemini calls through the agy CLI (Gemini subscription) instead of Vertex
AGY_MODELS = {FLASH: "gemini-3.8-flash-high", ARGON: "gemini-4-argon-high"}
AGY_CHUNK = 170000  # agy truncates a single stream-json message at ~194 KB (measured 2026-10-16)
GPT_MODEL = "gpt-6-sol"
VOLUME_CAP = 160_000      # chars of Volume VI kept (tail), so context stays bounded as the volume grows
PROGRESS_CAP = 12_000     # chars of graph/PROGRESS.md tail

RULES = """Operating rules (from ANY.md and the volumes; they override your defaults):
- Work from the supplied sources only and cite file + section for every reused result. Reuse, do not rediscover: if
  the archive already has a result under another name, say so and build on it.
- Type every premise NATIVE (follows from D/T/C and ANY's rulings), CONDITIONAL (an entered model contract) or
  PHYSICS-IMPORTED. Never present an imported premise as native.
- Proof standard (§119, §317.8): recovery of known physics counts as evidence only when near-miss alternatives are
  EXCLUDED by the stated premises. Name the near-misses.
- Nothing is "proven" until executed. Z3 certifies only the encoded finite real-algebraic family; UNKNOWN is not proof.
- Keep the framework's typed correspondence language (≃) and its separation of D, T, C and realized geometry.
- Graham's method (§476.7): mathematics is the normalization layer, not the result. Numbers, symbols and variables
  are themselves debated: for each number that carries weight, state what produced it (its relations and context)
  and question its physical value. "E=mc²" is not "1=1×2²". We are breaking physics down as much as solving it
  algebraically: relational mathematics, not only algebra.
- Graham (§480.6): "Ask the relations. Always point back to different forms of solving, reduction, expansion or
  simplification. Solve it not just through addition, but every other metric. The reasoning tells the story, not the
  numbers themselves." Never settle a question by stipulating one operation; solve it through several forms and say
  which relation each form answers to.
- Graham (2026-10-14, after §491): "Of course outside measurements are needed. Its not meant to be a know all. ANY is
  just a word without understanding. A and Y are contextual, so is N. Its about context. Its not about 'interrogate
  this single equation with ANY' its about applying its graph to the overall picture and filling in context on the
  unknown." So: an imported constant or measurement is expected context, not a failure of ANY; do not score rounds
  by "native vs not". Start from the unknown, lay the whole graph (all domains, volumes I-VI) over it, and report
  which relations around the unknown supply its context (what it connects to, what fixes it, what it explains).
  Keep the NATIVE/CONDITIONAL/IMPORTED typing as provenance labels only.
- Respect Graham's rulings recorded in the volumes (e.g. §476.7: a count is meaningful but not definitional; C is
  single-valued within a context but not in relation to A/N/Y).
- The whole repository is the research context. GPT runs inside it with read-only access: open volumes/, graph/
  and bridge/ files directly whenever a cited section or record matters. Other models: use the volume table of
  contents to locate earlier results and cite them by section.
- The research is one connected body: before proposing, check how the step bears on earlier sections, open items
  and rulings, and say what it changes upstream."""

CLAIMS_SPEC = """End with a fenced ```json block: a list of claims, each
{"id": "C1", "statement": exact mathematical statement, "premises": {"native": [...], "conditional": [...],
 "imported": [...]}, "near_miss": the alternative it must exclude, "encoding": how to encode it (sympy identity /
 z3 sat/unsat query / finite enumeration), "expected": the expected outcome, "falsifier": what result would refute it}.
At most 5 physics/mathematics claims. Prefer claims that could fail.
REQUIRED in addition (Graham: "ANY and physics run side by side"): one ANY-join claim per ANY ruling the section
uses, at least one in total, each {"id": "A1", "any_ruling": an id from ledger/rulings.yaml (e.g. R-COUNT, R-DPOT,
R-NUM, R-CONTEXT, P-CONE, R-TSELF), "verdict": "consistent" | "needs bridge" | "conflicts", "statement": how the
round's physics normalizes or tests that ruling, "bridge": the premise needed if the verdict is "needs bridge"}.
A round whose claims are physics only fails the method and is sent back."""


def read(path, cap=None):
    if not os.path.exists(path):
        return ""
    txt = open(path, encoding="utf-8").read()
    return txt[-cap:] if cap and len(txt) > cap else txt


def next_section():
    nums = [int(n) for n in re.findall(r"^#{1,2} §(\d+)", read(VOLUME), re.M)]
    return max(nums) + 1 if nums else 475


def volumes_toc():
    out = []
    for f in sorted(os.listdir(os.path.join(ROOT, "volumes"))):
        if f.endswith((".md", ".txt")):
            heads = [l.rstrip() for l in open(os.path.join(ROOT, "volumes", f), encoding="utf-8", errors="replace")
                     if l.startswith("## ")]
            out.append(f"--- volumes/{f} ---\n" + "\n".join(heads))
    return "\n".join(out)


def context(round_no, extra=()):
    prev = os.path.join(LOOP, "rounds", f"{round_no - 1:03d}", "claude_check.md")
    parts = [("ANY_CARD.md (the method on one page; follow it)", read(os.path.join(ROOT, "ANY_CARD.md"))),
             ("GRAPH_SHEET.md (the whole registry graph; cite its ids, keep its statuses)", read(os.path.join(ROOT, "GRAPH_SHEET.md"))),
             ("ANY.md (operating document)", read(os.path.join(ROOT, "ANY.md"))),
             ("Table of contents of ALL volumes (every section heading; cite and reuse them)", volumes_toc()),
             ("Volume VI (active; tail)", read(VOLUME, VOLUME_CAP)),
             ("graph/PROGRESS.md (tail)", read(os.path.join(ROOT, "graph", "PROGRESS.md"), PROGRESS_CAP)),
             ("loop/OPEN.md (open questions, Claude-maintained)", read(os.path.join(LOOP, "OPEN.md"))),
             (f"Claude's computational verdicts on round {round_no - 1}", read(prev) or "(none yet)")]
    for path in extra:
        parts.append((f"ANY graph record: {path}", read(os.path.join(ROOT, path), 40_000)))
    return "\n\n".join(f"===== {name} =====\n{body}" for name, body in parts)


def _token():
    if not PROJECT:
        raise SystemExit("Set ANY_VERTEX_PROJECT before using Vertex.")
    if vertex_disabled():
        raise SystemExit("VERTEX DISABLED (loop/spend.json vertex_disabled): use --agy, or Codex/GPT.")
    return subprocess.run([GCLOUD, "auth", "application-default", "print-access-token"],
                          capture_output=True, text=True, check=True).stdout.strip()


def open_cache(text, model=None):
    """Upload the round's shared context once as a Vertex cachedContents resource. On any failure the loop just
    sends the context inline as before."""
    model = model or MODEL
    pin, _ = PRICES.get(model, PRICES[ARGON])
    est_tokens = len(text) / 3
    create_usd = est_tokens / 1e6 * pin + est_tokens / 1e6 * STORAGE_PER_MTOK_HOUR.get(model, 4.5) * CACHE_TTL_S / 3600
    st = spend_state()
    if st["spent_usd"] + create_usd > st["cap_usd"]:
        raise SystemExit(f"SPEND CAP: cache creation (${create_usd:.2f}) would cross the cap.")
    url = f"https://aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/global/cachedContents"
    body = json.dumps({"model": f"projects/{PROJECT}/locations/global/publishers/google/models/{model}",
                       "contents": [{"role": "user", "parts": [{"text": text}]}],
                       "ttl": f"{CACHE_TTL_S}s"}).encode()
    try:
        req = urllib.request.Request(url, body, {"Authorization": f"Bearer {_token()}", "Content-Type": "application/json"})
        d = json.load(urllib.request.urlopen(req, timeout=600))
    except Exception as e:  # noqa: BLE001 - caching is an optimisation only
        detail = e.read().decode()[:300] if isinstance(e, urllib.error.HTTPError) else str(e)
        log(dict(time=datetime.datetime.now().isoformat(timespec="seconds"), step="cache_create", model=model,
                 ok=False, error=detail))
        return None
    tokens = d.get("usageMetadata", {}).get("totalTokenCount") or est_tokens
    spent = charge(model, tokens, 0, extra_usd=tokens / 1e6 * STORAGE_PER_MTOK_HOUR.get(model, 4.5) * CACHE_TTL_S / 3600)
    CACHE.update(text=text, name=d["name"], model=model)
    log(dict(time=datetime.datetime.now().isoformat(timespec="seconds"), step="cache_create", model=model, ok=True,
             cached_tokens=tokens, spent_usd_total=spent))
    return d["name"]


def close_cache():
    if not CACHE.get("name"):
        return
    try:
        req = urllib.request.Request(f"https://aiplatform.googleapis.com/v1/{CACHE['name']}",
                                     headers={"Authorization": f"Bearer {_token()}"}, method="DELETE")
        urllib.request.urlopen(req, timeout=120)
    except Exception:  # noqa: BLE001 - it expires on its own after the TTL
        pass
    CACHE.clear()


def log(entry):
    with open(os.path.join(LOOP, "ledger.jsonl"), "a") as f:
        f.write(json.dumps(entry) + "\n")


def agy_call(prompt, round_no, step, model):
    """One Gemini turn through the agy CLI. The prompt goes over stdin as stream-json, split into parts below agy's
    per-message limit, followed by a final message that asks for the answer. No Vertex spend."""
    parts = [prompt[i:i + AGY_CHUNK] for i in range(0, len(prompt), AGY_CHUNK)]
    lines = []
    for i, part in enumerate(parts):
        head = (f"[Prompt part {i + 1} of {len(parts)}. The parts together form ONE prompt. Do not use any tools. "
                f"Reply only: received {i + 1}]\n\n") if len(parts) > 1 else ""
        lines.append(json.dumps({"event": "user", "message": {"content": head + part}}))
    if len(parts) > 1:
        lines.append(json.dumps({"event": "user", "message": {"content":
            "All parts have been sent. Carry out the instructions of the complete prompt now and give your full answer "
            "in the requested format. Do not use any tools; work only from the text you were given."}}))
    t = time.time()
    for attempt in range(3):
        r = subprocess.run(["agy", "--input-format", "stream-json", "--output-format", "stream-json", "--model",
                            AGY_MODELS.get(model, model), "--print-timeout", "1800s", "-p="], input="\n".join(lines) + "\n", capture_output=True,
                           text=True, cwd=ROOT, timeout=3600)
        results = [json.loads(l)["result"] for l in r.stdout.splitlines() if l.startswith('{"event":"result"')]
        last = results[-1] if results else {}
        if last.get("status") == "SUCCESS" and last.get("response", "").strip():
            log(dict(time=datetime.datetime.now().isoformat(timespec="seconds"), round=round_no, step=step,
                     model="agy:" + AGY_MODELS.get(model, model), parts=len(parts), ok=True, seconds=round(time.time() - t, 1),
                     input_tokens=last.get("usage", {}).get("input_tokens"), output_tokens=last.get("usage", {}).get("output_tokens")))
            return last["response"]
        time.sleep(60 * (attempt + 1))
    log(dict(time=datetime.datetime.now().isoformat(timespec="seconds"), round=round_no, step=step, model="agy", ok=False,
             error=(last.get("error") or r.stderr[-300:] or "no result")))
    raise RuntimeError(f"agy: {step} failed")


def argon(prompt, round_no, step, temperature=0.4, max_tokens=32000, model=None):
    """One Vertex call (Flash by default, Argon with --argon), behind the spend cap; with --agy, one agy turn instead."""
    model = model or MODEL
    if AGY or vertex_disabled():
        return agy_call(prompt, round_no, step, model)
    cached = CACHE.get("name") if CACHE.get("model") == model and CACHE.get("text") and CACHE["text"] in prompt else None
    if cached:
        prompt = prompt.replace(CACHE["text"], "(The shared context for this round, ANY.md, the volumes, OPEN.md and "
                                                "the graph records, is the cached content given before this message.)")
    check_budget(model, prompt, max_tokens)
    token = _token()
    url = (f"https://aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/global/publishers/google/models/"
           f"{model}:generateContent")
    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
               "generationConfig": {"maxOutputTokens": max_tokens, "temperature": temperature}}
    if cached:
        payload["cachedContent"] = cached
    body = json.dumps(payload).encode()
    for attempt in range(4):
        t = time.time()
        req = urllib.request.Request(url, body, {"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        try:
            d = json.load(urllib.request.urlopen(req, timeout=1200))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and attempt < 3:
                time.sleep(30 * (attempt + 1))
                continue
            raise
        cand = d["candidates"][0]
        text = "".join(p.get("text", "") for p in cand["content"]["parts"] if not p.get("thought"))
        u = d.get("usageMetadata", {})
        spent = charge(model, u.get("promptTokenCount"),
                       (u.get("candidatesTokenCount") or 0) + (u.get("thoughtsTokenCount") or 0),
                       cached_tokens=u.get("cachedContentTokenCount") or 0)
        log(dict(spent_usd_total=spent, cached_tokens=u.get("cachedContentTokenCount"), time=datetime.datetime.now().isoformat(timespec="seconds"), round=round_no, step=step,
                 model=d.get("modelVersion"), prompt_tokens=u.get("promptTokenCount"),
                 output_tokens=u.get("candidatesTokenCount"), thought_tokens=u.get("thoughtsTokenCount"),
                 finish=cand.get("finishReason"), seconds=round(time.time() - t, 1)))
        return text
    raise RuntimeError(f"{model}: retries exhausted")


def gpt(prompt, round_no, step):
    """GPT-6 via Codex in an empty directory, read-only, high reasoning. Returns None when quota is exhausted."""
    work = os.path.join(LOOP, ".gpt_scratch")
    os.makedirs(work, exist_ok=True)
    out = os.path.join(work, f"r{round_no:03d}_{step}.txt")
    t = time.time()
    r = subprocess.run([CODEX, "exec", "--skip-git-repo-check", "--sandbox", "read-only", "-m", GPT_MODEL,
                        "-c", "model_reasoning_effort=high", "-o", out, "-"],
                       input=prompt, capture_output=True, text=True, cwd=ROOT, timeout=3600)
    blob = r.stdout + r.stderr
    used = re.search(r"tokens used\s*\n?\s*([\d,]+)", blob)
    served = re.search(r"^model: (\S+)", blob, re.M)
    text = open(out).read().strip() if os.path.exists(out) else ""
    log(dict(time=datetime.datetime.now().isoformat(timespec="seconds"), round=round_no, step=step,
             model=served.group(1) if served else GPT_MODEL, tokens_used=used.group(1) if used else None,
             ok=bool(text), seconds=round(time.time() - t, 1),
             error=None if text else blob.strip()[-300:]))
    return text or None


def ruling_ids():
    import yaml
    return {r["id"] for r in yaml.safe_load(open(os.path.join(ROOT, "ledger", "rulings.yaml"), encoding="utf-8"))}


def focus_items(focus):
    """Required item labels in a round focus: T1, T5(c), FINAL DELIVERABLE, ... (line starts only)."""
    labels = re.findall(r"^(T\d+(?:\([a-z]\))?|FINAL DELIVERABLE|ORGANIZING QUESTION)(?!\w)", focus, re.M)
    return list(dict.fromkeys(labels))


def any_joins(claims):
    """The ANY-join claims among `claims`: a known ledger ruling id and one of the three verdicts."""
    ids = ruling_ids()
    return [c for c in claims if isinstance(c, dict) and c.get("any_ruling") in ids
            and c.get("verdict") in ("consistent", "needs bridge", "conflicts")]


def claims_from(text):
    blocks = re.findall(r"```json\s*(.*?)```", text, re.S)
    for b in reversed(blocks):
        try:
            data = json.loads(b)
            return data if isinstance(data, list) else data.get("claims", [])
        except json.JSONDecodeError:
            continue
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int)
    ap.add_argument("--no-gpt", action="store_true")
    ap.add_argument("--no-cache", action="store_true", help="send the shared context inline instead of caching it")
    ap.add_argument("--argon", action="store_true", help="use Gemini 4 Argon instead of 3.8 Flash (costs ~5x)")
    ap.add_argument("--agy", action="store_true", help="run the Gemini steps through the agy CLI (Gemini subscription), not Vertex")
    ap.add_argument("--focus", default="")
    ap.add_argument("--section", type=int, help="section number (default: next after the volume's last), so a round can start before the previous one is integrated")
    ap.add_argument("--extra", nargs="*", default=[], help="extra repo files (e.g. graph records) added to context")
    ap.add_argument("--gpt-develop", action="store_true", help="GPT-6 (Codex) writes the develop draft")
    ap.add_argument("--debate", type=int, default=3,
                    help="auditor<->developer exchanges before the revision (1 = single audit)")
    a = ap.parse_args()
    global MODEL, AGY
    if a.argon:
        MODEL = ARGON
    rounds = os.path.join(LOOP, "rounds")
    os.makedirs(rounds, exist_ok=True)
    existing = sorted(int(d) for d in os.listdir(rounds) if d.isdigit())
    n = a.round or (existing[-1] + 1 if existing else 1)
    out = os.path.join(rounds, f"{n:03d}")
    os.makedirs(out, exist_ok=True)
    sec = a.section or next_section()
    ctx = context(n, a.extra)
    AGY = a.agy or vertex_disabled()
    if not a.no_cache and not AGY:
        import atexit
        open_cache(ctx)
        atexit.register(close_cache)
    focus = f"\nGraham's focus for this round: {a.focus}\n" if a.focus else ""
    meta = dict(round=n, section=sec, started=datetime.datetime.now().isoformat(timespec="seconds"), developer=None)

    def save(name, text):
        open(os.path.join(out, name), "w", encoding="utf-8").write(text)

    propose = argon(f"""You are the PROPOSER in an automated research round on Graham's ANY framework. Two models
(Gemini 4 Argon and GPT-6) alternate; Claude then executes every claim in sympy/z3 and integrates the result.
{RULES}
{focus}
TASK: choose the single most determining next question, taking the active volume's latest "next solve", loop/OPEN.md
and Claude's last verdicts into account (a claim Claude refuted must not be re-proposed unchanged). State why it is
the most determining, which earlier sections it connects to, then work it: derivation, typed premises, near-misses.
{CLAIMS_SPEC}

{ctx}""", n, "propose")
    save("01_propose.md", propose)

    def develop_prompt():
        return f"""You are the DEVELOPER in an automated research round on Graham's ANY framework. Another model
proposed the step below. Challenge it first (circularity, premises imported but labelled native, results the
archive already has, overreach of scope), then develop what survives into a draft of Volume VI §{sec}, written in
the volume's established voice and structure (numbered subsections, typed premises, executed-vs-claimed separation,
"Weak points" paragraph). Do not claim execution: Claude runs the claims afterwards.
{RULES}
{CLAIMS_SPEC}

===== PROPOSAL =====
{propose}

{ctx}"""

    develop = gpt(develop_prompt(), n, "develop") if a.gpt_develop else None
    dev = "gpt" if develop else MODEL
    if not develop:
        develop = argon(develop_prompt(), n, "develop", temperature=0.7)
    meta["developer"] = dev
    save("02_develop.md", develop)

    audit_prompt = f"""You are the ADVERSARIAL AUDITOR in an automated research round on Graham's ANY framework. You did
not write the draft below; your job is to break it. Check every citation against the supplied sources, every
NATIVE label, every "excludes" claim (is the near-miss really excluded, or only unencoded?), and whether the claims
can be encoded as stated. List REQUIRED FIXES (numbered, concrete) and OPTIONAL improvements, then give a verdict:
integrate / integrate after fixes / reject (with reason).
{RULES}

===== DRAFT §{sec} =====
{develop}

{ctx}"""
    audit = None if a.no_gpt else gpt(audit_prompt, n, "audit")   # one GPT call per round: the cross-family audit
    meta["auditor"] = "gpt" if audit else MODEL
    if not audit:
        audit = argon(audit_prompt, n, "audit", temperature=0.3)
    transcript = [f"## Audit 1 ({meta['auditor']})\n\n{audit}"]
    for k in range(2, a.debate + 1):     # direct model-to-model debate; Claude reads only the saved transcript
        reply = argon(f"""You wrote the draft of Volume VI §{sec}. The independent auditor challenged it. Answer point by
point: concede what is right (say how you would fix it), rebut what is wrong with source citations, and raise any
objection the auditor missed. Do not rewrite the section yet.
{RULES}

===== YOUR DRAFT =====
{develop}

===== DEBATE SO FAR =====
{chr(10).join(transcript)}

{ctx}""", n, f"debate{k}_developer", temperature=0.4)
        transcript.append(f"## Developer reply {k - 1} ({MODEL})\n\n{reply}")
        counter_prompt = f"""{audit_prompt}

===== DEBATE SO FAR (you are the auditor; the developer has replied) =====
{chr(10).join(transcript)}

Respond to the developer's reply: withdraw objections it answered, press the ones it did not, add new ones. End with
an updated REQUIRED FIXES list and verdict."""
        counter = None if a.no_gpt or meta["auditor"] != "gpt" else gpt(counter_prompt, n, f"debate{k}_audit")
        if not counter:
            counter = argon(counter_prompt, n, f"debate{k}_audit", temperature=0.3)
        transcript.append(f"## Audit {k} ({'gpt' if meta['auditor'] == 'gpt' and counter else MODEL})\n\n{counter}")
    audit = "\n\n".join(transcript)
    meta["debate_exchanges"] = a.debate
    save("03_audit.md", audit)

    revise_prompt = f"""You wrote the draft of Volume VI §{sec} below; an independent auditor's findings follow. Apply
every required fix you accept and rebut (with source citations) any you reject. Output the FINAL section text,
then a short "Rebuttals" list, then the final claims.
{RULES}
{CLAIMS_SPEC}

===== YOUR DRAFT =====
{develop}

===== AUDIT =====
{audit}

{ctx}"""
    revise = argon(revise_prompt, n, "revise", temperature=0.4)
    save("04_revise.md", revise)
    items, supp_claims = focus_items(a.focus), []
    if items:
        check = argon(f"""Below are the REQUIRED items of Graham's focus and a FINAL SECTION. For each item label, answer
whether the final section addresses that item substantively (its own derivation, verdict or answer, not a passing
mention). Output ONLY a fenced ```json object mapping each label to true or false.

===== FOCUS =====
{a.focus}

===== FINAL SECTION =====
{revise}""", n, "scope_check", temperature=0.0)
        m = re.search(r"\{.*\}", check, re.S)
        try:
            covered = json.loads(m.group(0)) if m else {}
        except json.JSONDecodeError:
            covered = {}
        missing = [t for t in items if covered.get(t) is not True]
        meta["scope"] = {t: ("covered" if t not in missing else "missing") for t in items}
        if missing:
            supplement = argon(f"""Your final Volume VI §{sec} below omitted these REQUIRED focus items: {", ".join(missing)}.
Do not narrow the scope. Write the missing parts now as additional subsections of §{sec} (same rules, compute every
number twice, imports cited), then a final ```json claims list for the new material only, including ANY-join claims.
{RULES}
{CLAIMS_SPEC}

===== FOCUS =====
{a.focus}

===== FINAL SECTION =====
{revise}""", n, "scope_supplement", temperature=0.4)
            save("04c_scope_supplement.md", supplement)
            supp_claims = claims_from(supplement) or []
            save("04_revise_pre_scope.md", revise)
            body = re.sub(r"```json.*?```", "", supplement, flags=re.S).rstrip()
            revise = revise.rstrip() + "\n\n" + body + "\n"
            save("04_revise.md", revise)
            meta["scope"].update({t: "supplemented" for t in missing})
            print(f"round {n}: scope supplement for {', '.join(missing)}", file=sys.stderr)
    claims = (claims_from(revise) or claims_from(develop)) + supp_claims
    joins = any_joins(claims)
    if not joins:
        repair = argon(f"""Your final claims for Volume VI §{sec} contain no valid ANY-join claim. Output ONLY a fenced
```json list of ANY-join claims in this format (ruling ids must exist in ledger/rulings.yaml: {", ".join(sorted(ruling_ids()))}):
{CLAIMS_SPEC.split("REQUIRED in addition", 1)[1]}
Base each verdict on the section below; do not repeat the physics claims.

===== FINAL SECTION =====
{revise}""", n, "any_join_repair", temperature=0.3)
        save("04b_any_join_repair.md", repair)
        joins = any_joins(claims_from(repair))
        claims = claims + joins
    meta["any_join"] = [f"{c['any_ruling']}: {c['verdict']}" for c in joins] or "MISSING"
    if not joins:
        print(f"WARNING round {n}: no valid ANY-join claim even after repair; method rule failed", file=sys.stderr)
    save("claims.json", json.dumps(claims, indent=2, ensure_ascii=False))
    meta.update(finished=datetime.datetime.now().isoformat(timespec="seconds"), claims=len(claims))
    save("meta.json", json.dumps(meta, indent=2))
    print(f"round {n} (§{sec}) done: developer={dev}, {len(claims)} claims -> {out}")


if __name__ == "__main__":
    sys.exit(main())
