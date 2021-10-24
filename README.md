documerica
==========

This repository holds JSON(L) artifacts and a few scripts related to managing
archival data from the EPA's [DOCUMERICA](https://en.wikipedia.org/wiki/Documerica)
program.

Contents:

* `*.sort.json.gz`: A compressed "raw" JSON collection of API results from the National Archives,
pertaining to DOCUMERICA
* `documerica.jsonl`: A filtered JSONL collection of DOCUMERICA records, munged
for use with the Twitter bot
* `missing.txt`: A newline-delimited list of National Archive IDs (NAIDs) for DOCUMERICA
records that are missing photographic scans
* `make_db.py`: A Python script that creates `documerica.db` from `documerica.jsonl`
* `bot/`: The Twitter bot
