from typing import Protocol


class TokenService(Protocol):
    def create_token(self, user_id: str, email: str) -> str: ...
