python=/tmp/python

all: info format check unit itest

info:
	PYTHONPATH=./src/main/python:/home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/ $(python) -m site

itest:
	PYTHONPATH=./src/main/python:/home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/ $(python) -m pytest src/test/python/bd_to_dot/oo

unit:
	PYTHONPATH=./src/main/python:/home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/ $(python) -m pytest src/test/python/bd_to_dot/dot

test: itest unit
	
format:
	autopep8 -ri src

check:
	flake8 src
	pyflakes src
	pycodestyle src
