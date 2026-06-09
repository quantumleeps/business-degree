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
2. **Written section** — the actual teaching. Multiple short subsections,
   plain-English first, then the precise/technical framing. Use an
   engineering or systems analogy where one genuinely clarifies.
3. **Visual section** — an inline, interactive or animated SVG/Canvas/JS
   visual that *shows* the concept (e.g. a draggable supply/demand graph, an
   animated accounting-equation balance, a CVP break-even chart). No external
   libraries; vanilla JS + SVG/Canvas only so it renders anywhere.
4. **Quiz** — 5–8 questions (mix of multiple-choice and short numeric/text).
   The quiz renders, accepts answers, and on submit POSTs results to the
   local recorder (see Step 4) OR, if offline, writes a results JSON the user
   can import. Never reveal correct answers in the page or page source.

## Step 3 — Write the answer key SEPARATELY

Write correct answers to `lessons/<address>.answers.json` (NOT embedded in
the HTML). Schema in `references/answer-key-format.md`. This is the only file
the guard hook protects. You may freely *create* it now; you may not *read*
an existing one later without an approval token. Because the key is not in
the HTML, grading happens server-side via the recorder script, keeping you
honest about my performance.

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

## Step 5 — Tell the user how to view it

Point them at `lessons/<address>-<slug>.html` and remind them they can run
`uv run scripts/serve.py` to enable quiz recording, and open
`harness/results.html` to see performance.

## What NOT to do

- Don't put correct answers anywhere in the HTML or its comments.
- Don't read an existing `*.answers.json` to "double-check" — that's what the
  approval gate is for. If you need it, ask the user to approve.
- Don't add external CDN dependencies to the lesson artifact.
- Don't build lessons the user didn't request.

See the two reference files for exact templates.
