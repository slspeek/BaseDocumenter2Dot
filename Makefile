
.PHONY: test info
python=/tmp/python

info:
	PYTHONPATH=./src/main/python $(python) -m site
	which soffice

test:
	PYTHONPATH=./src/main/python:/home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/ $(python) -m pytest
