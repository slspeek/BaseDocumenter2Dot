
.PHONY: test info
python=/usr/libreoffice6.4/program/python

info:
	which soffice
	PYTHONPATH=./src/main/python $(python) -m site

test:
	PYTHONPATH=./src/main/python:/home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/ $(python) -m pytest
