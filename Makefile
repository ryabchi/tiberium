PYTHONPATH = ./
CODE = apps tiberium tests

.PHONY: init test lint format

test:
	$(PYTHONPATH) pytest --verbosity=2 --showlocals --strict --log-level=DEBUG --cov=$(CODE) $(args) -k "$k"

lint:
	black --target-version py37 --skip-string-normalization --line-length=120 --check $(CODE)
	pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	mypy $(CODE)
	pytest --dead-fixtures --dup-fixtures

format:
	isort --apply --recursive $(CODE)
	black --target-version py37 --skip-string-normalization --line-length=120 $(CODE)
