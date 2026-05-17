.PHONY: run check format test test-real

run:
	uv run uvicorn app.main:app --reload --port 8000

check: format-check lint typecheck test

format:
	uv run ruff format app/ tests/

format-check:
	uv run ruff format --check app/ tests/

lint:
	uv run ruff check app/ tests/

typecheck:
	uv run mypy app/

test:
	uv run pytest -x -q --ignore=tests/golden --ignore=tests/integration

test-real:
	uv run pytest -x -q -m "real_llm"
