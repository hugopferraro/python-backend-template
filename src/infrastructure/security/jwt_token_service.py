from datetime import timedelta

from src.application.auth.token_service import TokenService
from src.infrastructure.security.jwt import create_access_token


class JwtTokenService:
    def create_token(self, user_id: str, email: str) -> str:
        return create_access_token(email, user_id, timedelta(minutes=20))
