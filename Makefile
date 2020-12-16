python=/tmp/python
PYTHONPATH=./src/main/python:/home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/

all: info format check itest unit

info:
	PYTHONPATH=$(PYTHONPATH) $(python) -m site

itest:
	PYTHONPATH=$(PYTHONPATH) $(python) -m pytest -v src/test/python/bd_to_dot_test/oo

unit:
	PYTHONPATH=$(PYTHONPATH) $(python) -m pytest -v src/test/python/bd_to_dot_test/dot

test: itest unit

format:
	autopep8 -ri src

check:
	flake8 src
	pycodestyle src

view:
	BD_VIEW=1 PYTHONPATH=$(PYTHONPATH) $(python) -m pytest -v src/test/python/bd_to_dot_test/dot/test_objects.py::test_view
