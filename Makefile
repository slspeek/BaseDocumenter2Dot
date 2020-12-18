python=/tmp/python
target=target
dist=$(target)/dist
stage=$(dist)/bd2dot_oxt/
lib=$(stage)/python/pythonpath
build=$(target)/build
PYTHONPATH=./src/main/python:/home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/

all: info format check itest unit oxt

.ONESHELL:
prepare:
	-mkdir -p $(build)
	cp -r src $(build)

.ONESHELL:
info: prepare
	cd $(build)
	PYTHONPATH=$(PYTHONPATH) $(python) -m site

.ONESHELL:
itest: prepare
	cd $(build)
	PYTHONPATH=$(PYTHONPATH) $(python) -m pytest -v src/test/python/bd_to_dot_test/oo

.ONESHELL:
unit: prepare
	cd $(build)
	PYTHONPATH=$(PYTHONPATH) $(python) -m pytest -v src/test/python/bd_to_dot_test/dot

test: itest unit

format:
	autopep8 -ri src

check:
	flake8 src

.ONESHELL:
view: prepare
	cd $(build)
	BD_VIEW=1 PYTHONPATH=$(PYTHONPATH) $(python) -m pytest -v src/test/python/bd_to_dot_test/dot/test_objects.py::test_view

clean:
	-@find src -type d -name __pycache__ -exec rm -rf '{}' \;
	-@rm -rf $(target)
	@echo $(target) was removed

.ONESHELL:
oxt:
	-mkdir -p $(lib) $(dist) $(build)
	python -m pip install graphviz \
	--ignore-installed --target $(lib)
	cp src/main/python/main.py $(stage)/python
	cp -r src/main/python/bd_to_dot $(lib)
	cp -r src/main/resources/oometadata/* $(stage)
	cp LICENSE $(stage)
	cd $(stage)
	zip -r ../bd2dot.oxt .
	unzip -t ../bd2dot.oxt
