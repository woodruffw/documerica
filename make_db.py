#!/usr/bin/env python3

# make_db: make documerica.db from documeria.jsonl

import json
import re
import sqlite3
from contextlib import closing
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_DOCUMERICA_JSONL = _HERE / "documerica.jsonl"
_DOCUMERICA_DB = _HERE / "documerica.db"

_PARENS = re.compile(r"\(([^)]*)\)")

_DOCUMERICA_SCHEMA = """
    CREATE TABLE documerica (
        naid INTEGER UNIQUE NOT NULL,
        title TEXT,
        author TEXT NOT NULL,
        created TEXT,
        url TEXT NOT NULL,
        tweeted INTEGER NOT NULL
    )
"""


def find_best_picture(files):
    for file in files:
        if file["@type"] == "primary" and file["@mime"] == "image/jpeg":
            return file["@url"]
    return None


def normalize_author(author):
    # Sometimes the author isn't known.
    if author is None:
        return "Unattributed"

    # Authors are normally `Lastname, Firstname`, but sometimes have some
    # additional bits including trailing dates or "photographer".
    # We also preserve the `(Preferred Name)`, if present.
    # Examples:
    #   Aleksandrowicz, Frank J. (Frank John), 1921-
    #   Daniels, Gene, photographer
    #   Duncan, Patricia D., 1932-
    components = author.split(",")

    last_name = components[0]
    first_name = components[1]

    preferred = _PARENS.search(first_name)
    if preferred:
        first_name = _PARENS.sub("", first_name)
        preferred_name = preferred.group(1)
        return f"{first_name.strip()} {last_name.strip()} ({preferred_name.strip()})"
    else:
        return f"{first_name.strip()} {last_name.strip()}"


if __name__ == "__main__":
    assert _DOCUMERICA_JSONL.is_file(), f"Fatal: missing: {_DOCUMERICA_JSONL}"
    assert not _DOCUMERICA_DB.exists(), f"Fatal: already exists: {_DOCUMERICA_DB}"

    db = sqlite3.connect(_DOCUMERICA_DB)

    with db:
        db.execute(_DOCUMERICA_SCHEMA)

    skipped, inserted = 0, 0
    with _DOCUMERICA_JSONL.open() as io, closing(db.cursor()) as cur:
        for line in io:
            record = json.loads(line)
            if not record["files"]:
                skipped += 1
                continue

            url = find_best_picture(record["files"])
            assert url is not None, f"no URL for {record['naid']}"

            author = normalize_author(record["author"])

            cur.execute(
                "INSERT INTO documerica VALUES (?, ?, ?, ?, ?, ?)",
                (record["naid"], record["title"], author, record["date"], url, False),
            )
            inserted += 1

    db.commit()
    db.close()

    print(f"Done: {inserted=}, {skipped=}")
