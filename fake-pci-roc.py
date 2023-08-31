#!/usr/bin/env python3
"""Generate fake PCI ROC traffic."""

import csv
import os
from pathlib import Path
import sys
import tempfile

output_path = Path("output")

top_lines = [
    b"""Scan Results,02/28/2023 at 16:24:43 (GMT-0500),,,,,,,,,,,,,,,,,,,,,,,\n""",
    b""""Securisea, Inc.",201 Spear Street,Suite 1100,San Francisco,California,United States of America,94105,,,,,,,,,,,,,,,,,,\n""",
    b"""Josh Daymont,secur3sd,Manager,,,,,,,,,,,,,,,,,,,,,,\n""",
    b""",,,,,,,,,,,,,,,,,,,,,,,,\n""",
    b"""Launch Date,Client,Active Hosts,Total Hosts,Type,Status,Reference,Scanner Appliance,Duration,Scan Title,Asset Groups,IPs,Excluded IPs,Option Profile,,,,,,,,,,,\n""",
    b"""08/31/2022 at 08:19:13 (GMT-0500),ASV Lab Test 2022,1,1,On-demand,Finished,scan/1661951953.32810,"64.39.98.9 (Scanner 12.11.33-1, Vulnerability Signatures 2.5.571-2)",12:38:59,ASV Lab Test 2022  .180 Website rev1,,72.1.207.180,,Low BandwidthPayment Card Industry (PCI) Options,,,,,,,,,,,\n""",
    b""",,,,,,,,,,,,,,,,,,,,,,,,\n""",
    b"""IP,DNS,NetBIOS,OS,IP Status,QID,Title,Type,Severity,Port,Protocol,FQDN,SSL,CVE ID,Vendor Reference,Bugtraq ID,Threat,Impact,Solution,Exploitability,Associated Malware,Results,PCI Vuln,Instance,Category\n""",
]

sample = b"""72.1.207.180,No registered hostname,,CentOS release 6.x,"host scanned, found vuln",11771,Title,Vuln,5,8080,tcp,,,<<CVEID>>,S2-045,96729,Threat,A remote attacker c,Solution,Exploitability,Associated Malware,Results,yes,,CGI\n"""


def new_file(tfh):
    """Close file if open and start a new one."""
    if tfh is not None:
        tfh.close()
    return tempfile.NamedTemporaryFile(
        suffix=".csv", prefix="tmp-", dir="output", delete=False
    )


def main():
    csv.field_size_limit(sys.maxsize)
    with open(output_path / "nvd-data.csv", newline="") as fh:
        reader = csv.reader(fh, dialect="excel")
        next(reader)
        tfh = None
        for rownum, cve in enumerate(reader, start=1):
            if tfh is None or (rownum % 10_000 == 0):
                tfh = new_file(tfh)
                tfh.writelines(top_lines)
            tfh.write(sample.replace(b"<<CVEID>>", str(cve[0]).encode("utf-8")))
        tfh.close()


if __name__ == "__main__":
    main()
