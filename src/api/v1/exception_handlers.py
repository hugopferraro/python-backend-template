from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.v1.problems.api_problem import ApiProblem
from src.domain.exceptions.domain_exception import DomainException

async def _domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    status = exc.error_code().http_status()
    problem = ApiProblem.from_domain_exception(exc, status=status, instance=request.url.path)
    return JSONResponse(status_code=status, content=problem.model_dump(mode="json"))


async def _request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    problem = ApiProblem.from_validation_errors(exc.errors(), instance=request.url.path)
    return JSONResponse(status_code=422, content=problem.model_dump(mode="json"))


async def _unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    problem = ApiProblem(
        type="about:blank",
        title="INTERNAL_SERVER_ERROR",
        status=500,
        detail="An unexpected error occurred.",
        error_code="INTERNAL_SERVER_ERROR",
        instance=request.url.path,
    )
    return JSONResponse(status_code=500, content=problem.model_dump(mode="json"))


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainException, _domain_exception_handler)
    app.add_exception_handler(RequestValidationError, _request_validation_handler)
    app.add_exception_handler(Exception, _unhandled_exception_handler)
