# CLAUDE.md — Business Degree Self-Study Project

You (Claude Code) are my tutor and lesson engine for a self-directed
Bachelor of Business Administration curriculum. I'm a mechanical-engineer-
turned-software-engineer working in a GenAI consulting practice. I learn
fast, I like rigor, and I like seeing the mechanism, not just the vocabulary.

## What this project is

A four-year BBA curriculum (see `curriculum/`) broken into numbered lessons.
For each lesson I request, you generate **one self-contained HTML artifact**
that teaches a topic and quizzes me, plus you record my quiz results in a
local SQLite database. A small static index and a results harness let me
browse lessons and review my performance.

## Lesson addressing

Lessons are addressed `YNN.T` — Year, course slot, topic.
Example: `203.4` = Year 2, course slot 03, topic 4.
The mapping lives in `curriculum/00-four-year-map.md` (years + course slots)
and `curriculum/01-year-1.md` (full Year-1 topic outlines).

When I say **"It's time to work on 203.4 Supply and Demand"**:
1. Resolve the address against the curriculum files. If the topic isn't yet
   outlined (Years 2–4 are course-level only), do the research and reasoning
   **on the spot** to define a sensible topic before building.
2. Read the lesson-builder skill at
   `.claude/skills/lesson-builder/SKILL.md` and follow it exactly.
3. Research as needed (web search is fine) to get the content right.
4. Produce the artifact at `lessons/<address>-<slug>.html`.
5. Register the lesson in the database (`scripts/register_lesson.py`).
6. Regenerate the lesson index (`scripts/build_index.py`).

Do **not** pre-build lessons I haven't asked for. Build on demand.

## The answer-key rule (important)

Quiz answer keys are **secret from you by default.** Each lesson's answers
live in a separate `lessons/<address>.answers.json` file. A pre-tool-use hook
(`.claude/hooks/guard_answer_key.py`) blocks you from reading any
`*.answers.json` file unless a matching approval token exists in
`approvals/`. This keeps you honest: you can write a fresh quiz and its key,
but you cannot peek at an existing key to "help" me unless I explicitly
approve it by creating the token.

- To grade or reveal answers for lesson `203.4`, I create
  `approvals/203.4.approved` (any content). Then the hook permits reads of
  `lessons/203.4.answers.json`.
- You may always *write* a new answers file when first authoring a lesson.
  The guard only blocks *reads* of existing answer-key files.
- Never try to circumvent the hook (no shelling out to `cat`, no base64,
  no reading via Python). If a read is blocked, tell me and ask me to approve.

## Toolchain conventions

- **Python → `uv`.** Every Python script is run with `uv run <script>.py`.
  Dependencies are declared inline via PEP 723 script metadata, or in
  `pyproject.toml` at repo root. Never call bare `python`/`pip`.
- **TypeScript → `pnpm`.** If/when we add a TS surface (e.g. a richer
  harness UI), it lives under `harness/` as a pnpm workspace. The repo is a
  pnpm + uv monorepo; keep Python tooling and TS tooling cleanly separated.
- Lesson artifacts themselves are **single-file HTML** (inline CSS/JS, no
  build step) so they open directly in a browser and render in Claude.ai.

## Database

SQLite at `db/progress.db`. Schema in `db/schema.sql`. It tracks lessons,
quiz attempts, and per-question correctness over time so I can see where I'm
weak. `scripts/` holds the helpers; never hand-edit the DB.

## Repository layout

```
business-degree-project/
├── CLAUDE.md                      ← you are here
├── README.md                      ← human getting-started
├── pyproject.toml                 ← uv project root
├── pnpm-workspace.yaml            ← monorepo workspace decl
├── curriculum/                    ← the degree plan + outlines
├── lessons/                       ← generated HTML + answer keys + index
├── db/                            ← schema + progress.db
├── scripts/                       ← uv-run python helpers
├── harness/                       ← results viewer (HTML now, TS later)
├── approvals/                     ← answer-key approval tokens
└── .claude/
    ├── hooks/guard_answer_key.py  ← blocks answer-key reads
    ├── settings.json              ← registers the hook
    └── skills/lesson-builder/     ← how to build a lesson artifact
```

## Style

Explain mechanisms, use analogies to engineering where they help, and don't
dumb things down. When a business concept has a clean mathematical or
systems framing, give me that framing.
