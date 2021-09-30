.PHONY: docs
install:
	pip install -r requirements.txt
	python setup.py install
lint:
	pip install flake8
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
test:
	pip install -r requirements.txt
	pip install pytest
	pytest
docs:
	make -C docs/ html
	firefox docs/_build/html/index.html &
install-env:
	python3 -m venv env
