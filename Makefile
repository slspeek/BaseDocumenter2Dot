
.PHONY: test
python=/tmp/python

test:
	PYTHONPATH=./src/main/python $(python) -m pytest
