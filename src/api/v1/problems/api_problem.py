from __future__ import annotations

import os
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from src.domain.exceptions.domain_exception import DomainException


class InvalidParam(BaseModel):
    name: str
    reason: str


class ApiProblem(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    error_code: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    invalid_params: list[InvalidParam] | None = None
    instance: str | None = None

    @classmethod
    def from_domain_exception(
        cls,
        exc: DomainException,
        status: int,
        instance: str | None = None,
    ) -> "ApiProblem":
        error_code = exc.error_code().code()
        invalid_params = (
            [InvalidParam(name=e.field, reason=e.message) for e in exc.errors()]
            if exc.errors()
            else None
        )
        return cls(
            type=_type_uri(error_code),
            title=error_code,
            status=status,
            detail=str(exc),
            error_code=error_code,
            invalid_params=invalid_params,
            instance=instance,
        )

    @classmethod
    def from_validation_errors(
        cls,
        errors: list[dict],
        instance: str | None = None,
    ) -> "ApiProblem":
        invalid_params = [
            InvalidParam(
                name=".".join(str(loc) for loc in err["loc"]),
                reason=err["msg"],
            )
            for err in errors
        ]
        return cls(
            type=_type_uri("validation-error"),
            title="VALIDATION_ERROR",
            status=422,
            detail="Request validation failed.",
            error_code="VALIDATION_ERROR",
            invalid_params=invalid_params,
            instance=instance,
        )


def _type_uri(error_code: str) -> str:
    base = os.getenv("API_BASE_URL", "about:blank")
    if base == "about:blank":
        return base
    return f"{base}/errors/{error_code.lower().replace('_', '-')}"
