from __future__ import annotations
from dataclasses import dataclass, field

from src.application.behaviour.request import Request
from src.api.v1.schemas.user_schemas import UserResponse


@dataclass
class ListUsersRequest(Request[list[UserResponse]]):
    search: str | None = field(default=None)
