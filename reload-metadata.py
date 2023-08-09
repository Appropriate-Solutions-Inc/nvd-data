"""Load all metadata in the ./data directory into a SQLite3 databse."""
# Copyright © 2023 Appropriate Solutions, Inc. All rights reserved.

import csv
from pathlib import Path
import sqlite3

base_dir = Path(".")
data_dir = base_dir / "data"
db_dir = base_dir / "db"
db_dir.mkdir(exist_ok=True)
db_path = db_dir / "nvd-metadata.db"


def create_db(conn) -> None:
    """Create the database.

    Safe to call on each invocation.
    The lastModifiedDate is likely the only thing we'll use.
    """
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS meta(importable, last_modified_date, file_size, zip_size, gz_size, sha256)"
    )
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_cve_id ON meta (importable)")
    cur.close()
    conn.commit()


def load_metadata(conn) -> None:
    """Load all metadata into the database."""
    cur = conn.cursor()

    for meta_path in data_dir.glob("*.meta"):
        data = []
        data.append(meta_path.stem)
        for line in meta_path.read_text().splitlines():
            els = line.split(":")
            data.append(":".join(els[1:]))

        cur.execute(
            "INSERT INTO meta "
            "(importable, last_modified_date, file_size, zip_size, gz_size, sha256) VALUES "
            "(?, ?, ?, ?, ?, ?);",
            data,
        )

        conn.commit()


conn = sqlite3.connect(db_path)
create_db(conn)
load_metadata(conn)
