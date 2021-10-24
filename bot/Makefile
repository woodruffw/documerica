.PHONY: env
env:
	test -d env || python3 -m venv env
	. env/bin/activate && \
		pip install --upgrade pip && \
		pip install -r requirements.txt
