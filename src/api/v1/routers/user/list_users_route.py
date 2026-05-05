from fastapi import APIRouter, Depends

from src.api.v1.dependencies.mediator import get_mediator, get_user_repository
from src.api.v1.dependencies.oauth2 import login_required
from src.api.v1.schemas.user_schemas import UserDetailResponse
from src.application.behaviour.mediator import Mediator
from src.application.usecases.user.list_users_request import ListUsersRequest
from src.domain.repositories.user_domain_repository import UserDomainRepository

router = APIRouter()


@router.get("/", response_model=list[UserDetailResponse])
def list_(
    search: str | None = None,
    _=Depends(login_required),
    mediator: Mediator = Depends(get_mediator),
    repository: UserDomainRepository = Depends(get_user_repository),
):
    return mediator.send(ListUsersRequest(search=search), repository=repository)
