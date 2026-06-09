#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Grade a quiz attempt against its (gated) answer key and store results.

Can be used two ways:

1) As a library, called by scripts/serve.py when a lesson POSTs an attempt.
2) Standalone, to import an offline attempt JSON the browser downloaded:

       uv run scripts/record_attempt.py --import 203.4.attempt.json

Grading reads lessons/<address>.answers.json. NOTE: this script runs as part
of YOUR (the human's) tooling, not as a Claude tool call, so it is not
subject to the answer-key guard hook — the hook only restricts Claude's own
file reads. That's intentional: the recorder must see the key to grade.
"""
import argparse
import json
import pathlib
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "progress.db"
LESSONS = ROOT / "lessons"


def load_key(address: str) -> dict:
    path = LESSONS / f"{address}.answers.json"
    if not path.exists():
        raise FileNotFoundError(f"No answer key for {address} at {path}")
    return json.loads(path.read_text())


def _match(q: dict, given) -> bool:
    t = q.get("type")
    correct = q.get("correct")
    if given is None or correct is None:
        return False
    if t == "mc":
        return str(given).strip().lower() == str(correct).strip().lower()
    if t == "num":
        try:
            return abs(float(given) - float(correct)) <= float(q.get("tolerance", 0))
        except (TypeError, ValueError):
            return False
    if t == "text":
        g = str(given).strip().lower()
        accepted = correct if isinstance(correct, list) else [correct]
        return g in [str(a).strip().lower() for a in accepted]
    return False


def grade(address: str, answers: dict) -> dict:
    key = load_key(address)
    results, correct_count, weak = [], 0, []
    for q in key["questions"]:
        qid = q["qid"]
        given = answers.get(qid)
        ok = _match(q, given)
        correct_count += int(ok)
        if not ok and q.get("topic"):
            weak.append(q["topic"])
        results.append({
            "qid": qid, "topic": q.get("topic"),
            "given": given, "is_correct": int(ok),
            "explanation": q.get("explanation", ""),
        })
    total = len(key["questions"])
    return {
        "address": address,
        "correct": correct_count,
        "total": total,
        "score_pct": round(100.0 * correct_count / total, 1) if total else 0.0,
        "weak_topics": sorted(set(weak)),
        "results": results,
    }


def store(graded: dict) -> None:
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO attempts (address, correct, total, score_pct) VALUES (?,?,?,?)",
        (graded["address"], graded["correct"], graded["total"], graded["score_pct"]),
    )
    attempt_id = cur.lastrowid
    for r in graded["results"]:
        cur.execute(
            """INSERT INTO question_results
               (attempt_id, address, qid, topic, given, is_correct)
               VALUES (?,?,?,?,?,?)""",
            (attempt_id, graded["address"], r["qid"], r["topic"],
             str(r["given"]), r["is_correct"]),
        )
    con.commit()
    con.close()


def record(address: str, answers: dict) -> dict:
    graded = grade(address, answers)
    store(graded)
    return graded


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--import", dest="imp", help="path to an offline attempt JSON")
    args = ap.parse_args()
    if args.imp:
        payload = json.loads(pathlib.Path(args.imp).read_text())
        out = record(payload["address"], payload["answers"])
        print(json.dumps(out, indent=2))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
