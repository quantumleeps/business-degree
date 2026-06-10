---
name: lesson-builder
description: Use this skill whenever the user asks to build, generate, or "work on" a numbered business lesson (e.g. "it's time to work on 203.4", "build lesson 107.5", "make the Supply and Demand lesson"). It defines the exact structure of a lesson HTML artifact — written teaching section, visual section, and gated quiz — plus how to register the lesson in the progress database and rebuild the index. Trigger this even when the user just gives a lesson address with no other instruction.
---

# Lesson Builder

Build one self-contained HTML lesson artifact for a single curriculum topic,
register it in the progress database, and rebuild the lesson index.

## Step 0 — Resolve the address

Parse the lesson address `YNN.T` against the curriculum:
- `curriculum/00-four-year-map.md` for year + course slot meaning
- `curriculum/01-year-1.md` for full Year-1 topic outlines

If the topic is already outlined, use that scope. If it's a Year 2–4 topic
that only exists at the course level, research the topic now (web search is
allowed) and define a focused, single-lesson scope before proceeding.
State the resolved title and scope to the user in one line before building.

## Step 1 — Research the content

Get the substance right. For factual/economic/accounting content, verify
definitions and standard formulas. Keep it accurate; this is a real
curriculum, not a vibe. Cite nothing inside the artifact, but don't invent.

## Step 2 — Build the artifact

Write a single HTML file to `lessons/<address>-<slug>.html`
(e.g. `lessons/107.5-segmentation-targeting-positioning.html`).
Use the structure in `references/artifact-template.md`. It MUST contain,
in this order:

1. **Header** — lesson address, title, and one-line "why this matters."
2. **Written section ("Learn")** — the actual teaching. Multiple short
   subsections, plain-English first, then the precise/technical framing.
   Teach in the discipline's own language and standard framings, as a
   college course would — do **not** reach for engineering or systems
   analogies (mass balances, rate-vs-state, signal/control metaphors);
   they add a translation layer the user has asked to avoid.
3. **Visual section(s) ("See it")** — one or **several** inline, interactive
   or animated SVG/Canvas/JS visuals that *show* the concept (e.g. a
   draggable supply/demand graph, an animated accounting-equation balance, a
   CVP break-even chart). No external libraries; vanilla JS + SVG/Canvas only
   so it renders anywhere.
4. **Quiz ("Check yourself")** — 5–8 questions (mix of multiple-choice and
   short numeric/text). The quiz renders, accepts answers, and on submit
   POSTs results to the local recorder (see Step 4) OR, if offline, writes a
   results JSON the user can import. Never reveal correct answers in the page
   or page source. After grading, the page renders per-question ✓/✗ feedback
   in place from the `/record` response (the template has the handler) —
   right/wrong flags and explanations come only from the server, post-attempt.

## Depth calibration — college course level

Every section targets the depth of a good undergraduate course: lecture +
assigned textbook reading + problem set, not a blog post or explainer video.
Concretely:

**Learn** — cover mechanism, formalism, and edge cases, with at least one
fully worked numeric example. Always include the actual formulas/identities
and use them, not just name them.

- Too shallow: "Price elasticity measures how sensitive quantity demanded
  is to price. Elastic goods respond a lot; inelastic goods respond little."
- On target: define point and arc elasticity with formulas, compute one from
  real numbers, show why revenue rises with a price cut when |ε| > 1 (and
  derive it: MR = P(1 + 1/ε)), and note the edge cases (perfectly
  elastic/inelastic, why elasticity varies along a linear demand curve).

**See it** — this is where complexity gets cheap: an interaction can teach a
second-order effect that would take paragraphs of prose. Don't simplify the
model to simplify the visual — keep the full college-level model and let
sliders/drag handles carry the cognitive load. Build **multiple visuals**
when the topic has more than one mechanism worth isolating; one visual per
mechanism beats one overloaded visual.

- Example (supply & demand lesson): (a) draggable curves showing equilibrium
  shift with live P*/Q* readout; (b) an elasticity slider that redraws the
  revenue rectangle as price changes; (c) a tax-wedge tool that splits
  incidence between buyer and seller as relative elasticities change.
- Example (balance sheet lesson): (a) a transaction simulator where each
  posted transaction animates both sides of A = L + E staying balanced;
  (b) a ratio dashboard (current ratio, debt-to-equity) that recomputes live
  as the user edits line items.

**Check yourself** — exam-level, not reading-check. Target mix across the
5–8 questions: 1–2 recall/definition, 2–3 application ("which scenario
is…", "what happens to X when Y"), 2–3 multi-step computation with realistic
numbers (the kind that requires writing something down, e.g. "compute COGS
under FIFO from this purchase ledger", not "2 + 2 inventory").

## Step 3 — Write the answer key SEPARATELY

Write correct answers to `lessons/<address>.answers.json` (NOT embedded in
the HTML). Schema in `references/answer-key-format.md`. This is the only file
the guard hook protects. You may freely *create* it now; you may not *read*
an existing one later without an approval token. Because the key is not in
the HTML, grading happens server-side via the recorder script, keeping you
honest about my performance.

Every question MUST carry an `explanation` that teaches the concept — it's
shown in place under missed questions after grading, so write it to reteach,
not just to state the right option.

## Step 4 — Register & wire up results

Run, with uv:
```bash
uv run scripts/register_lesson.py --address <address> --title "<title>" \
    --file lessons/<address>-<slug>.html
uv run scripts/build_index.py
```
`register_lesson.py` inserts/updates the lesson row. `build_index.py`
regenerates `lessons/index.html`. The quiz submits attempts to
`scripts/record_attempt.py` (run via the tiny local server in
`scripts/serve.py`), which grades against the answers file and stores each
attempt in `db/progress.db`.

Then verify the artifact per **"Verifying the artifact"** below — mock
`/record`; never submit a real attempt.

## Step 5 — Tell the user how to view it

Point them at `lessons/<address>-<slug>.html` and remind them they can run
`uv run scripts/serve.py` to enable quiz recording, and open
`harness/results.html` to see performance. Offer to commit (one commit per
lesson — see CLAUDE.md "Commit cycle"); stage with the pathspec
`git add 'lessons/<address>'*` so the shell command never names the answer
key (naming an unapproved key file in a command trips the guard hook).

## Verifying the artifact — mock the recorder, never POST for real

The quiz POSTs to `/record`, which **writes a real attempt into
`db/progress.db`** and skews the user's scores and topic-mastery stats. A
build-verification submit is indistinguishable from a real attempt, so:

- **Never verify by submitting the quiz against the live recorder.**
- Test the submit flow headlessly with a route mock instead — real page,
  real server, fake grading, zero DB writes:

```python
# uv run --with playwright python - <<'EOF' ... (server running on 8753)
def mock(route):
    body = route.request.post_data_json
    qids = list(body["answers"].keys())
    route.fulfill(json={
        "address": body["address"], "correct": 1, "total": len(qids),
        "score_pct": 0, "weak_topics": ["t"],
        "results": [{"qid": q, "topic": "t", "given": None,
                     "is_correct": i % 2, "explanation": "mock"}
                    for i, q in enumerate(qids)]})
page.route("**/record", mock)
```

Then assert each `.q` gets `right`/`wrong` classes and a `.fb` feedback node.
If a test attempt ever does land in the DB, do not delete it yourself
(hand-editing the DB is forbidden) — tell the user the attempt id and let
them remove it and rerun `build_index.py`.

## What NOT to do

- Don't put correct answers anywhere in the HTML or its comments.
- Don't read an existing `*.answers.json` to "double-check" — that's what the
  approval gate is for. If you need it, ask the user to approve.
- Don't add external CDN dependencies to the lesson artifact.
- Don't build lessons the user didn't request.
- Don't POST test attempts to `/record` — see "Verifying the artifact" above.

See the two reference files for exact templates.
