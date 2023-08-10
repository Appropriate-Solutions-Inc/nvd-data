"""Update downloads based on metadata information.

Don't run more than once every two hours. 
Daily is probably sufficient.

Add API key to header during requests.

- Phase 1:
  - Find all meta importable's where needs_update is 0.
  - Download new meta files. 
  - See if lastModifiedDate is newer.
    - No: Keep going.
    - Yes: 
      - Save Meta file.
      - Download data file.
      - Update database metadata.
      - Set needs_update to 1.
- Phase 2: 
  - Find all importable's with needs_update 1.
    - Import/update data.
    - Set needs_update to 0.

- Manual:
  - Update repo.

"""
# Copyright © 2023 Appropriate Solutions, Inc. All rights reserved.

from datetime import datetime
import os
from pathlib import Path
import sqlite3
import sys
import time

import requests

base_dir = Path(".")
data_dir = base_dir / "data"
db_dir = base_dir / "db"
db_dir.mkdir(exist_ok=True)
db_path = db_dir / "nvd-metadata.db"
base_url = "https://nvd.nist.gov/feeds/json/cve/1.1"
api_key = os.environ["NVD_API_KEY"]
url_timeout = 60  # Website can take a LONG time to respond.
api_sleep = 7  # Seven second timeout on URL request without API key.
if api_key:
    api_sleep = 0.7


def all_importables(conn: sqlite3.Connection) -> list[str]:
    """Return sorted list of importables."""
    cur = conn.cursor()
    cur.execute("SELECT importable FROM meta;")
    importables = [x[0] for x in cur.fetchall()]
    importables.sort()
    return importables


def importables_to_check(conn: sqlite3.Connection) -> list[str]:
    """Return sorted list of importables where `needs_update` is 0."""
    cur = conn.cursor()
    cur.execute("SELECT importable FROM meta WHERE needs_update=0;")
    importables = [x[0] for x in cur.fetchall()]
    importables.sort()
    return importables


def download(url: str) -> str:
    """Download data from URL.

    Use
    """
    headers = {}
    if api_key:
        headers["apiKey"] = api_key

    resp = requests.get(url, headers=headers, timeout=url_timeout)
    time.sleep(api_sleep)
    return resp


def download_metas(importables: list[str]) -> None:
    """Download meta files into ./data directory."""
    print(f"Download timeout: {api_sleep}s")
    for importable in importables:
        url = f"{base_url}/{importable}.meta"
        print(f"Downloading: {url}.")
        resp = download(url)
        if resp.status_code != 200:
            print(f"Failure code: {resp.status_code}")
            continue

        meta = resp.text
        file_path = data_dir / f"{importable}.meta"
        print(f"Storing: {file_path}.")
        file_path.write_text(meta)


def load_meta_modified_date(path: Path) -> datetime:
    """Load lastModifiedDate from .meta file."""
    els = path.read_bytes().splitlines()[0].decode("utf-8").split(":")
    mod_date = ":".join(els[1:])
    return datetime.strptime(mod_date, "%Y-%m-%dT%H:%M:%S%z")


def get_stored_modified_date(conn: sqlite3.Connection, name: str) -> datetime:
    """Load last_modified_date from meta table."""
    cur = conn.cursor()
    cur.execute("SELECT last_modified_date FROM meta WHERE importable=?", [name])
    mod_date = cur.fetchone()[0]
    return datetime.strptime(mod_date, "%Y-%m-%d %H:%M:%S%z")


def set_needs_update(conn: sqlite3.Connection, importable: str):
    """Set `needs_update` to 1 (true) in meta table for importable."""
    cur = conn.cursor()
    cur.execute(
        "UPDATE meta SET needs_update=1 WHERE importable=?;",
        [importable],
    )
    conn.commit()


def check_metadata(conn: sqlite3.Connection):
    """Flag new metadata files.

    Compare meta file lastModifiedDate against database.
    Set `needs_update` to 1 (true) if date is newer.
    """
    modified_count = 0
    for importable in all_importables(conn):
        name = f"{importable}.meta"
        path = data_dir / name
        print(f"Checking meta data for: {importable}.")
        file_date = load_meta_modified_date(path)
        db_date = get_stored_modified_date(conn, importable)

        if file_date > db_date:
            print(f"{importable} needs update.")
            set_needs_update(conn, importable)
            modified_count += 1

    print(f"Number of modified files: {modified_count}.")


def main():
    conn = sqlite3.connect(db_path)
    if not (importables := importables_to_check(conn)):
        print("No importables need checking")
        sys.exit(0)

    print(f"Number of importables to process: {len(importables)}.")
    # RGAC!! download_metas(importables)

    check_metadata(conn)


if __name__ == "__main__":
    main()
