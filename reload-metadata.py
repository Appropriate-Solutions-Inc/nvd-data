"""Load all metadata in the ./data directory into a SQLite3 database.

   Loading recent.json.gz and modified.json.gz is redundant, 
   but we're only doing this until December and it is not worth 
   digging into the data to ensure coverage.

"""
# Copyright © 2023 Appropriate Solutions, Inc. All rights reserved.

from datetime import datetime
from pathlib import Path
import sqlite3

base_dir = Path(".")
data_dir = base_dir / "data"
db_dir = base_dir / "db"
db_dir.mkdir(exist_ok=True)
db_path = db_dir / "nvd-metadata.db"


def recreate_db(conn: sqlite3.Connection) -> None:
    """Re-create the database."""
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS meta;")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS meta "
        "(importable, last_modified_date, file_size, zip_size, gz_size, sha256, "
        "needs_update INTEGER DEFAULT 0 NOT NULL);"
    )
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_cve_id ON meta (importable);")
    cur.close()
    conn.commit()


def parse_datetime(date_time: str) -> datetime:
    """Parse 2023-08-04T03:01:58-04:00 into Python date/time."""
    dt = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S%z")
    return dt


def load_metadata(conn: sqlite3.Connection) -> None:
    """Load importable and meta data into the database.

    - Parse lastModifiedDate as datetime with timezone offset.
    """
    cur = conn.cursor()

    for meta_path in data_dir.glob("*.meta"):
        data = []
        data.append(meta_path.stem)
        for line in meta_path.read_text().splitlines():
            els = line.split(":")
            data.append(":".join(els[1:]))

        # data[1] is lastModifiedDate
        data[1] = parse_datetime(data[1])

        cur.execute(
            "INSERT INTO meta "
            "(importable, last_modified_date, file_size, zip_size, gz_size, sha256) VALUES "
            "(?, ?, ?, ?, ?, ?);",
            data,
        )

        conn.commit()


conn = sqlite3.connect(db_path)
recreate_db(conn)
load_metadata(conn)
