from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.api.v1.dependencies.mediator import get_mediator, get_user_repository, get_token_service
from src.application.auth.token_service import TokenService
from src.application.behaviour.mediator import Mediator
from src.application.usecases.auth.login_request import LoginRequest
from src.api.v1.schemas.auth_schemas import Token
from src.domain.repositories.user_domain_repository import UserDomainRepository

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    mediator: Mediator = Depends(get_mediator),
    repository: UserDomainRepository = Depends(get_user_repository),
    token_service: TokenService = Depends(get_token_service),
):
    return mediator.send(
        LoginRequest(email=form_data.username, password=form_data.password),
        repository=repository,
        token_service=token_service,
    )
