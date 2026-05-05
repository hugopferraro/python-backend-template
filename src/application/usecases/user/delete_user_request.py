from __future__ import annotations
from dataclasses import dataclass

from src.application.behaviour.request import Request
from src.api.v1.schemas.user_schemas import UserResponse


@dataclass
class DeleteUserRequest(Request[UserResponse | None]):
    identifier: str
