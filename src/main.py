# src/main.py
import logging
import time
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from src.api.v1.exception_handlers import register_exception_handlers
from src.core.config import get_settings
from src.api.v1.routers.router import api_router
from src.core.logging import setup_logging, request_context, get_logger

settings = get_settings()

# Setup logging before creating the src
setup_logging()

logger = get_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
    swagger_css_url="https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css"
)

app.include_router(api_router, prefix="/api/v1")
register_exception_handlers(app)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    token = request_context.set({
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "client_ip": request.client.host if request.client else None,
    })

    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000)

    response.headers["X-Request-ID"] = request_id

    # Enrich context with response data before logging
    ctx = request_context.get()
    ctx["status_code"] = response.status_code
    ctx["duration_ms"] = duration_ms

    # Single log line per request with all accumulated context
    level = "WARNING" if response.status_code >= 400 else "INFO"
    logger.log(
        logging.getLevelName(level),
        "%s %s %s %dms",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    request_context.reset(token)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
