# NVD Data

Python project to manage files from the NIST NVD data feed.

NOTE: This is a quick toss-away project as the NVD batch data feeds are being retired on 2023-12-15.

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
