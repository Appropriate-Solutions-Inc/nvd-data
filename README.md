# NVD Data

Python project to manage files from the NIST NVD data feed.

NOTE: This is a quick toss-away project as the NVD
[data feeds](https://nvd.nist.gov/vuln/data-feeds)
are being retired on 2023-12-15.


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


### Load metadata
Load all metadata files into a SQLite3 database.

Only do this one time.

```bash
python load_metadata.py
```
