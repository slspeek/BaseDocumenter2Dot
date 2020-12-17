python=/tmp/python
PYTHONPATH=./src/main/python:/home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/

all: info clean format check itest unit oxt

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

clean:
	-find src -type d -name __pycache__ -exec rm -rf '{}' \;
	-rm -rf build

target=target
stage=$(dist)/bd2dot_oxt/
lib=$(stage)/python/pythonpath
dist=$(target)/dist

.ONESHELL:
oxt:
	-mkdir -p $(lib) $(dist)
	python -m pip install graphviz \
	--ignore-installed --target $(lib)
	cp src/main/python/main.py $(stage)/python
	cp -r src/main/python/bd_to_dot $(lib)
	cp -r src/oometadata/* $(stage)
	cp LICENSE $(stage)
	cd $(stage)
	zip -r ../bd2dot.oxt .
	unzip -t ../bd2dot.oxt
