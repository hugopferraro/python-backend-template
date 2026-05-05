from __future__ import annotations
from dataclasses import dataclass, field

from src.application.behaviour.request import Request
from src.api.v1.schemas.user_schemas import UserResponse


@dataclass
class UpdateUserRequest(Request[UserResponse | None]):
    identifier: str
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    email: str | None = field(default=None)
