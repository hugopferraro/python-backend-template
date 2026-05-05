from __future__ import annotations
from dataclasses import dataclass

from src.application.behaviour.request import Request
from src.api.v1.schemas.auth_schemas import Token


@dataclass
class LoginRequest(Request[Token]):
    email: str
    password: str
