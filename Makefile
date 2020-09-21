all: clean build test install

clean:
	rm -Rf *.egg-info
	rm -Rf build
	rm -Rf dist
	rm -Rf .pytest_cache
	rm -f .coverage

build: clean
	python3 setup.py sdist

test:
	pytest -vv
	coverage run --source=domination -m pytest
	coverage report --omit="*/test*"

linter:
	pip install -r requirements.txt
	pylint domination --output-format=text --ignore-patterns=test --fail-under=8

install: build clean
	pip install -r requirements.txt
	python setup.py install

deploy-pip: install
	pip install twine
	twine upload -u bameza -p ${PYPI_PWD} --skip-existing dist/*
