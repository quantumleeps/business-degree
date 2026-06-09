#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Initialize the progress database from db/schema.sql.

Usage:
    uv run scripts/init_db.py
"""
import pathlib
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "progress.db"
SCHEMA = ROOT / "db" / "schema.sql"


def main() -> None:
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA.read_text())
    con.commit()
    con.close()
    print(f"Initialized {DB}")


if __name__ == "__main__":
    main()
