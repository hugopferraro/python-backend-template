# Python Backend Template

A production-ready Python backend template built on Clean Architecture principles.
Includes a full User CRUD as a reference implementation.

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
docker compose exec api uv run alembic upgrade head
```

**5. Access the app**

- **API docs:** http://localhost:8000/docs
- **Grafana:** http://localhost:3000

---

## Architecture

The project follows **Clean Architecture** with four layers. Dependencies only point inward — infrastructure and API depend on the application/domain, never the reverse.

```
src/
├── api/               # Delivery layer (FastAPI routers, schemas, exception handlers)
├── application/       # Use cases, mediator, DTOs
├── domain/            # Entities, value objects, repository protocols, exceptions
├── infrastructure/    # Database, repositories, JWT, hashing
└── core/              # Settings, logging setup
```

### Domain

Pure Python — no framework dependencies.

- **Entities** (`domain/entities/`) — aggregate roots. `UserDomainEntity` holds value objects and enforces invariants.
- **Value Objects** (`domain/vo/`) — immutable, self-validating. Each VO raises a `DomainException` on invalid input (e.g. `UserID`, `Email`, `PersonalInfo`, `HashedPassword`).
- **Repository protocols** (`domain/repositories/`) — `Protocol` interfaces that define what persistence operations are available. Infrastructure implements them; the domain never imports infrastructure.
- **Typed exceptions** (`domain/exceptions/`) — `DomainException` carries an `ErrorCode`. Each error code enum member owns both its string code and its HTTP status as a tuple value:

```python
class UserErrorCode(Enum):
    NOT_FOUND      = ("USER_NOT_FOUND",      404)
    ALREADY_EXISTS = ("USER_ALREADY_EXISTS", 409)
    ...
    def code(self) -> str:    return self.value
    def http_status(self) -> int: return self._status
```

### Application

Orchestrates domain objects. No HTTP or ORM knowledge.

- **Mediator** (`application/behaviour/mediator.py`) — dispatches a `Request[T]` to its registered `Handler[Req, Res]`. Supports a composable `PipelineBehavior` chain (e.g. exception handling behavior wraps every handler).
- **`@use_case` decorator** — auto-registers a handler class in the global registry. No manual wiring needed.
- **Use cases** (`application/usecases/`) — one `Request` + one `Handler` per operation. Handlers are stateless; per-request dependencies (e.g. repository) are passed via `mediator.send(..., repository=repo)`.
- **`UserReadDTO`** — application-layer data transfer object returned by read repository methods. Carries all entity value objects plus DB-generated `created_at`/`updated_at` timestamps, keeping the domain entity free of persistence concerns.

### Infrastructure

Implements domain protocols.

- **SQLAlchemy 2.0** ORM models with `server_default=func.now()` for timestamps.
- **Alembic** migrations under `src/infrastructure/database/migrations/`.
- **`UserRepository`** implements `UserDomainRepository`. Read methods (`find_by_identifier`, `list`) return `UserReadDTO`; write methods (`save`, `delete`) work with `UserDomainEntity`.
- **JWT** (`infrastructure/security/jwt.py`) — token encode/decode via `python-jose`.
- **Hashing** (`infrastructure/security/hash.py`) — bcrypt via `passlib`.

### API

FastAPI delivery layer. Translates HTTP ↔ application.

- **One file per endpoint** under `api/v1/routers/`. Each file defines a bare `router = APIRouter()`. The `__init__.py` aggregator sets the prefix and tags and includes all endpoint routers.
- **Schemas** (`api/v1/schemas/`) — Pydantic models. `UserResponse` (create/update, no timestamps) and `UserDetailResponse` (get/list/me, includes `created_at`/`updated_at`).
- **Error format** — RFC 9457 `ApiProblem` JSON response for all `DomainException`s. The exception handler calls `exc.error_code().http_status()` directly — no mapping dict needed.
- **Auth dependency** — `login_required` (`api/v1/dependencies/oauth2.py`) decodes the JWT bearer token and injects the current user.
- **Request context middleware** — attaches a `request_id` (from `X-Request-ID` header or generated), method, path, client IP, status code, and duration to every log line. Emits one structured log line per request.

---

## Tech Stack

| Concern | Libraries |
|---|---|
| API | FastAPI, Pydantic v2, Uvicorn |
| Database | PostgreSQL 16, SQLAlchemy 2.0, Alembic |
| Auth | `passlib[bcrypt]`, `python-jose` |
| Logging | `structlog`, Grafana Loki, Promtail, Grafana |
| Containerisation | Docker, Docker Compose |
| Package management | `uv` |
