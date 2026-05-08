include .env
export

.PHONY: install
	@pip install --upgrade uv
	@uv sync

.PHONY: up
up:
	@docker compose up --build -d

.PHONY: migrate
migrate:
	@uv run alembic upgrade head