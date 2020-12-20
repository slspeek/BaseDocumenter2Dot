libreoffice=/tmp/program
python=$(libreoffice)/python
unopkg=$(libreoffice)/unopkg
target=target
dist=$(target)/dist
stage=$(dist)/bd2dot_oxt/
lib=$(stage)/python/pythonpath
build=$(target)/build
test_output=$(build)/test-output
PYTHONPATH=./src/main/python:./vendor:/home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/

all: info check itest unit oxt


prepare:
	-mkdir -p $(build) $(test_output)
	cp -r src $(build)
	cp -r src/test/resources/output-dir $(build)

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

.ONESHELL:
check: format
	flake8 src && pycodestyle src

.ONESHELL:
view: prepare
	cd $(build)
	BD_VIEW=1 PYTHONPATH=$(PYTHONPATH) $(python) -m pytest -v src/test/python/bd_to_dot_test/dot/test_objects.py::test_view

clean:
	-@find src -type d -name __pycache__ -exec rm -rf '{}' \;
	-@rm -rf $(target)
	#-@rm -rf src/test/resources/output_dir/graphs
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

install_oxt:
	-$(unopkg) remove "com.github.slspeek.BaseDocumenter2Dot"
	$(unopkg) add -s $(dist)/bd2dot.oxt

open_test_db: prepare
	cd $(build)
	$(libreoffice)/soffice src/test/resources/testdb/testdb.odb \
													src/test/resources/testdb/testdb_broken_query.odb
