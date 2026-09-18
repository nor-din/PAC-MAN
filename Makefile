CONFIG = config.json

install:
	pip install uv
	uv sync

run:
	uv run python3 pac-man.py $(CONFIG)

debug:
	uv run python3 -m pdb pac-man.py $(CONFIG)

clean:
	rm -rf .mypy_cache .venv
	rm -rf __pycache__ src/__pycache__
	rm -f *.pyc src/*.pyc

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict
