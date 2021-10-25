documerica
==========

This repository holds JSON(L) artifacts and a few scripts related to managing
archival data from the EPA's [DOCUMERICA](https://en.wikipedia.org/wiki/Documerica)
program.

Contents:

* `Makefile`: A Makefile with some convenience rules for rebuilding files
* `*.sort.json.gz`: A compressed "raw" JSON collection of API results from the National Archives,
pertaining to DOCUMERICA
* `documerica.jsonl`: A filtered JSONL collection of DOCUMERICA records, munged
for use with the Twitter bot
* `filter.jq`: A `jq` filter for transforming `*.sort.jsonl` into `documerica.jsonl`
* `missing.txt`: A newline-delimited list of National Archive IDs (NAIDs) for DOCUMERICA
records that are missing photographic scans
* `make_db.py`: A Python script that creates `documerica.db` from `documerica.jsonl`
* `bot/`: The Twitter bot

## License

The API results stored in the library are public domain.

All other material is under a [modified MIT License](./LICENSE).
