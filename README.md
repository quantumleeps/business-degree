# Business Degree — Self-Study Project

A self-directed Bachelor of Business Administration curriculum where **Claude
Code builds an interactive HTML lesson for each topic on demand**, quizzes
you, and tracks your performance in a local database — without being able to
peek at the answer keys unless you approve it.

## The idea

- The full curriculum lives in `curriculum/` (a four-year map + detailed
  Year-1 topic outlines).
- Each topic has an address like `203.4` (Year 2, course slot 03, topic 4).
- You say *"It's time to work on 203.4 Supply and Demand"* and Claude Code
  researches, builds `lessons/203.4-supply-and-demand.html` (teach + visual +
  quiz), writes a separate gated answer key, and registers it.
- Quiz results are graded and stored in `db/progress.db`. Browse lessons at
  `lessons/index.html`; see performance at `harness/results.html`.

## One-time setup

You need [`uv`](https://docs.astral.sh/uv/) installed. Then:

```bash
uv run scripts/init_db.py        # create db/progress.db from db/schema.sql
```

That's it for Python — every script declares its own deps inline (PEP 723)
and runs under `uv run`. (TypeScript via `pnpm` is reserved for a future
richer harness UI; nothing to install yet.)

## Daily loop

1. In Claude Code, from this directory, say e.g.
   **"It's time to work on 105.2 Cost behavior."**
   Claude builds the lesson and registers it.
2. Start the recorder so quizzes can save results:
   ```bash
   uv run scripts/serve.py
   ```
   Open `http://127.0.0.1:8753/lessons/index.html`, click into the lesson,
   learn, take the quiz. (If you open the HTML file directly without the
   server, the quiz downloads an attempt JSON you can import later with
   `uv run scripts/record_attempt.py --import <file>`.)
3. See how you're doing: `http://127.0.0.1:8753/harness/results.html`.

## The answer-key guard

Answer keys live in `lessons/<address>.answers.json`, **separate** from the
lesson HTML. A Claude Code hook (`.claude/hooks/guard_answer_key.py`,
registered in `.claude/settings.json`) blocks Claude from *reading* any answer
key unless you've created an approval token:

```bash
touch approvals/203.4.approved   # now Claude may read 203.4's answer key
```

Claude can always *write* a new key when first authoring a lesson; it just
can't read existing keys back without your say-so. The grader script
(`record_attempt.py`) is part of *your* tooling, not a Claude tool call, so it
reads keys freely to grade you — the guard only constrains Claude itself.

## Layout

| Path | What |
|------|------|
| `CLAUDE.md` | Instructions Claude Code follows |
| `curriculum/` | Four-year map + Year-1 outlines |
| `lessons/` | Generated HTML, answer keys, `index.html` |
| `db/` | `schema.sql` + `progress.db` |
| `scripts/` | uv-run helpers (init, register, record, serve, build_index) |
| `harness/` | `results.html` performance viewer |
| `approvals/` | Answer-key approval tokens you create |
| `.claude/` | Hook, settings, and the `lesson-builder` skill |

## Extending past Year 1

Years 2–4 are mapped at the course level in
`curriculum/00-four-year-map.md`. When you reach them, either ask Claude to
expand a course into the same numbered-outline format, or just request a
topic directly — the lesson-builder skill will research and scope it on the
spot.
