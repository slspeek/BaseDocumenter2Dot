python=/tmp/python

all: info format check test

info:
	PYTHONPATH=./src/main/python:/home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/ $(python) -m site

test:
	PYTHONPATH=./src/main/python:/home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/ $(python) -m pytest

format:
	autopep8 -ri src

check:
	flake8 src
	pyflakes src
	pycodestyle src
