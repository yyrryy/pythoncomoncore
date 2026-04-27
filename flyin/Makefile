.PHONY: install run debug clean lint lint-strict

install:
	pip install -r requirements.txt

run:
	python main.py maps/test.txt

debug:
	python -m pdb main.py maps/test.txt

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

lint:
	flake8 . --max-line-length=88 --extend-ignore=E203
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . --max-line-length=88 --extend-ignore=E203
	mypy . --strict