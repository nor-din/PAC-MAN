install:
	uv venv
	uv pip install -r requirements.txt

run:
	uv run python3 pac-man.py config.json

debug:
	uv run python3 -m pdb pac-man.py config.json

clean:
	rm -rf __pycache__ src/__pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .venv

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict
