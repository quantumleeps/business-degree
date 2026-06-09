#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Register (insert or update) a lesson in the progress database.

Usage:
    uv run scripts/register_lesson.py --address 203.4 \
        --title "Supply and Demand" --file lessons/203.4-supply-and-demand.html
"""
import argparse
import pathlib
import re
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "progress.db"

ADDR_RE = re.compile(r"^(?P<year>\d)(?P<slot>\d{2})\.(?P<topic>\d+)$")


def parse_address(address: str):
    m = ADDR_RE.match(address)
    if not m:
        return None, None, None
    return int(m["year"]), m["slot"], int(m["topic"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--address", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--file", required=True)
    args = ap.parse_args()

    year, slot, topic = parse_address(args.address)

    con = sqlite3.connect(DB)
    con.execute(
        """
        INSERT INTO lessons (address, title, file, year, course_slot, topic)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(address) DO UPDATE SET
            title=excluded.title,
            file=excluded.file,
            year=excluded.year,
            course_slot=excluded.course_slot,
            topic=excluded.topic,
            updated_at=datetime('now')
        """,
        (args.address, args.title, args.file, year, slot, topic),
    )
    con.commit()
    con.close()
    print(f"Registered lesson {args.address}: {args.title}")


if __name__ == "__main__":
    main()
