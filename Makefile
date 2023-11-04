.PHONY: setup format lint check clean ci 

setup:
	pip install -e .
	pip install -r requirements-dev.txt

format:
	black notebook_httpdbg

lint:
	black --check notebook_httpdbg
	flake8 notebook_httpdbg

check: lint

clean:
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf notebook_httpdbg.egg-info
	rm -rf venv
	rm -rf build
	rm -rf dist

ci:
	python -m pip install pip --upgrade
	python -m pip install setuptools wheel --upgrade
	pip install -r requirements-dev.txt
	pip install .
