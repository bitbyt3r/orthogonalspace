all: run

run: venv
	export RPM_MODE=false; \
	venv/bin/python setup.py install
	venv/bin/orthogonalspace -c contrib/conf.json

cli: venv
	venv/bin/python cli.py

tables: venv
	venv/bin/python ./create-table-migration.py

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	python3 -m venv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

clean:
	-rm -rf venv
	-find . -name \*.pyc -delete
	-find . -name __pycache__ -delete
	-rm -rf dist
	-rm *.rpm
	-rm -rf orthogonalspace.egg-info/
	-rm -rf build/

rpm: venv
	export RPM_MODE=true; \
	venv/bin/python setup.py bdist_rpm --release $(shell git rev-list $(shell git tag)..HEAD --count)

deps_rpm: venv
	venv/bin/python build-deps.py

venv/bin/crossbar: venv
	venv/bin/pip install crossbar
	venv/bin/crossbar init

crossbar: venv/bin/crossbar
	venv/bin/crossbar start
