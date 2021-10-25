#!/usr/bin/env python3

import os
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

import requests
import twitter


_HERE = Path(__file__).resolve().parent
_DOCUMERICA_DB = _HERE / "documerica.db"

_ONE_PHOTO = "SELECT * FROM documerica WHERE tweeted = 0 ORDER BY RANDOM() LIMIT 1"


def archives_url(naid):
    return f"https://catalog.archives.gov/id/{naid}"


if __name__ == "__main__":
    assert _DOCUMERICA_DB.is_file(), f"Fatal: missing: {_DOCUMERICA_DB}"

    # Fetch a random photo that hasn't been tweeted before.
    with closing(sqlite3.connect(_DOCUMERICA_DB)) as db:
        db.row_factory = sqlite3.Row

        with closing(db.cursor()) as cur:
            cur.execute(_ONE_PHOTO)
            photo = cur.fetchone()
            # Failure here indicates that we've tweeted every photo, and need
            # to reset the DB back to its initial state.
            if photo is None:
                cur.execute("UPDATE documerica SET tweeted = 0")
                db.commit()
                cur.execute(_ONE_PHOTO)
                photo = cur.fetchone()

        db.commit()

    # Fetch the photo's data from the National Archives.
    print(f"Posting: {photo['naid']} {photo['url']}")
    resp = requests.get(photo["url"])
    resp.raise_for_status()

    # Tweet it.
    api = twitter.Api(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_KEY_SECRET"),
        access_token_key=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )

    if photo["created"] is not None:
        created = datetime.fromisoformat(photo["created"])
        created = created.strftime("%Y-%m")
        tweet = f"Photographer: {photo['author']}, {created}"
    else:
        tweet = f"Photographer: {photo['author']}"

    with NamedTemporaryFile() as io:
        io.write(resp.content)
        io.flush()
        # For whatever reason, the chunked API consistently fails.
        # Our photos are hopefully always small enough to pass through
        # the non-chunked media API.
        media_id = api.UploadMediaSimple(io)
        api.PostMediaMetadata(media_id, photo["title"])
        api.PostUpdate(
            f"{tweet}\n\n{archives_url(photo['naid'])}",
            media=media_id,
        )

    # Update the tweet status for the photo we've just posted.
    with closing(sqlite3.connect(_DOCUMERICA_DB)) as db:
        with db:
            db.execute(
                "UPDATE documerica SET tweeted = 1 WHERE naid = ?", (photo["naid"],)
            )
        db.commit()
