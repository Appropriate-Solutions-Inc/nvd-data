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


def importables_to_check(conn) -> list[str]:
    """Find importables where `needs_update` is 0."""
    cur = conn.cursor()
    cur.execute("SELECT importable FROM meta WHERE needs_update=0")
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


def main():
    conn = sqlite3.connect(db_path)
    if not (importables := importables_to_check(conn)):
        print("No importables need checking")
        sys.exit(0)

    print(f"Number of importables to process: {len(importables)}.")
    download_metas(importables)


if __name__ == "__main__":
    main()
