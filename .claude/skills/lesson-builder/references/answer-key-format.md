# Answer Key Format

Each lesson's answer key is a SEPARATE file: `lessons/<address>.answers.json`.
It is the only file the guard hook protects from reads. The lesson HTML must
never contain these answers.

## Schema

```json
{
  "address": "203.4",
  "title": "Supply and Demand",
  "questions": [
    {
      "qid": "q1",
      "type": "mc",
      "correct": "c",
      "topic": "demand curve shifts",
      "explanation": "A change in consumer income shifts the entire demand curve, not movement along it."
    },
    {
      "qid": "q2",
      "type": "num",
      "correct": 12.5,
      "tolerance": 0.1,
      "topic": "equilibrium price",
      "explanation": "Set Qd = Qs and solve for P."
    },
    {
      "qid": "q3",
      "type": "text",
      "correct": ["surplus", "excess supply"],
      "topic": "disequilibrium",
      "explanation": "Price above equilibrium yields quantity supplied > quantity demanded."
    }
  ]
}
```

## Field notes

- `type`: `"mc"` | `"num"` | `"text"`.
- `correct`:
  - `mc`  → the correct option value (e.g. `"c"`).
  - `num` → a number; use `tolerance` for acceptable absolute error.
  - `text`→ a string OR array of acceptable strings (compared
    case-insensitively, trimmed).
- `topic`: short tag used to compute weak-topic feedback and per-topic mastery
  in the database. Reuse consistent tags across lessons in the same course.
- `explanation`: shown to the user only after grading, returned by the
  recorder — never embedded in the lesson page.

The grader (`scripts/record_attempt.py`) reads this file. The guard hook lets
Claude *create* it during authoring but blocks Claude from *reading* an
existing one unless `approvals/<address>.approved` exists.
