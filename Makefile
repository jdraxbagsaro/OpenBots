.PHONY: test run-mock

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

run-mock:
	PYTHONPATH=src python -m opendots.cli run --config opendots.example.toml --message "Hello, OpenDots."