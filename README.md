# NVD Data

Manage CVE data from the NIST NVD batch data feed.

NOTE: This is a quick toss-away project as the NVD batch data feeds are being retired on 2023-12-15.

The project was knocked together in a few hours to grab current CVE data for another project.

## URLs

- Batch [data feeds](https://nvd.nist.gov/vuln/data-feeds)
- [Vulnerabilities](https://nvd.nist.gov/developers/vulnerabilities)
  - cveId
  - lastModStartDate
  - lastModEndDate
- [Data Source](https://nvd.nist.gov/developers/data-sources)

## Installation

- Requires Poetry
- Clone the repository
- Run: `poetry shell`
- Run: `poetry install`

## Directories

- Data and metadata files are in the `./data` directory.
- Output files sent to the `./output` directory.
- A SQLite3 database file is maintained in the `./db` directory.

## Commands

### Convert all files to .csv

Output is in `./data/nvd-data.csv`.

```bash
python csv-all.py
```

### Re-load metadata
Tear down the existing metadata database and reload from the `.meta` files

```bash
python load_metadata.py
```

### Download and Update CVE Data

- Compare last modified time in the meta files against the database.
- Flag importables for update if date in file is later than date in the database.
- Download the `.json.gz` files associated with updated meta data.
- Update database that importable no longer needs updating.
- Manual step: Update repository.
