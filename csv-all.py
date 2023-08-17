#!/usr/bin/env python3
"""Flatten all data files in the ./data directory."""
# Copyright © 2023 Appropriate Solutions, Inc. All rights reserved.

import csv
import gzip
import json
from pathlib import Path


def cve_id(jsn: dict) -> str:
    """Extract the CVE ID."""
    return jsn["cve"]["CVE_data_meta"]["ID"]


base_dir = Path(".")
data_dir = base_dir / "data"
output_dir = base_dir / "output"
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "nvd-data.csv"

with open(output_path, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile, dialect="excel")
    csv_writer.writerow(["cve_id", "cve"])

    for gz_path in (Path(".") / "data").glob("*.json.gz"):
        print(f"Processing: {gz_path}")
        with gzip.open(gz_path) as ungz_path:
            cves = json.load(ungz_path)
            for cve in cves["CVE_Items"]:
                csv_writer.writerow([cve_id(cve), json.dumps(cve)])
