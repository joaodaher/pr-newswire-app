setup:
	@pip install -U pip uv

dependencies:
	@make setup
	@uv sync --group test --group crawler --group storage --group api

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

run-crawler:
	@echo "Running crawler ..."
	uv run python -m crawler.main

run-api:
	@echo "Running API ..."
	uv run uvicorn api.main:app --reload

run-web:
	@echo "Running web app ..."
	@cd web && npm run dev

# Docker commands
run-all:
	@echo "Building and starting Docker services..."
	@docker-compose up --build

clean-up:
	@echo "Stopping services and removing volumes..."
	@docker-compose down --volumes


.PHONY: setup dependencies update test check lint run-all clean-up
