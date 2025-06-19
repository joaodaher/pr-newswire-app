setup:
	@pip install -U pip uv

dependencies:
	@make setup
	@uv sync --group test --group crawler --group storage

update:
	@uv lock --upgrade

test:
	@make check
	@make lint
	@make unit

check:
	@uv lock --locked

lint:
	@echo "Checking code style ..."
	uv run ruff format --check .
	uv run ruff check .

style:
	@echo "Applying code style ..."
	uv run ruff format .
	uv run ruff check . --fix --unsafe-fixes

unit:
	@echo "Running unit tests ..."
	uv run pytest

.PHONY: setup dependencies update test check lint
