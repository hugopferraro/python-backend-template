# Python Backend Template

A production-ready Python backend template in Clean Architecture.
It includes a simple User CRUD as a reference implementation.

## Requirements

- Python **3.13**
- Docker & Docker Compose
- `uv` (recommended) or `pip`

## Quickstart

**1. Clone and install dependencies**

```bash
pip install --upgrade uv
uv sync
```

**2. Configure environment**

```bash
cp .env.example .env
```

**3. Start all services**

```bash
docker compose up --build -d
```

**4. Run database migrations**

```bash
docker compose exec template-api uv run alembic upgrade head
```

**5. Access the app**

- **API docs:** http://localhost:8000/docs
- **Grafana:** http://localhost:3000

## Architecture

- **Layered:** API routers -> domain services -> repositories -> SQLAlchemy models
- **Auth:** JWT tokens via `python-jose`, password hashing via `passlib[bcrypt]`
- **Errors:** Typed exceptions in services, caught and mapped to HTTP responses in routers
- **Logging:** Structured JSON logs in non-dev environments, colored text in dev. One log line per request with all context fields.

## Tech Stack

- **API:** FastAPI, Pydantic, Uvicorn
- **Database:** PostgreSQL 16, SQLAlchemy 2.0, Alembic
- **Auth:** passlib[bcrypt], python-jose
- **Logging:** Grafana, Loki, Promtail
- **Containerization:** Docker, Docker Compose
