from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.auth.token_service import TokenService
from src.application.behaviour.behaviors.exception_handling_behavior import ExceptionHandlingBehavior
from src.application.behaviour.mediator import Mediator
from src.domain.repositories.user_domain_repository import UserDomainRepository
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.database.session import get_db
from src.infrastructure.security.jwt_token_service import JwtTokenService

_mediator = Mediator(behaviors=[ExceptionHandlingBehavior()])
_token_service = JwtTokenService()


def get_mediator() -> Mediator:
    return _mediator


def get_user_repository(db: Session = Depends(get_db)) -> UserDomainRepository:
    return UserRepository(db)


def get_token_service() -> TokenService:
    return _token_service
