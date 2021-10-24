.PHONY: all
all: documerica.jsonl

documerica.jsonl: 1.sort.json 2.sort.json
	jq -c -f filter.jq $^ > $@

%.sort.json: %.sort.json.gz
	gunzip $<
