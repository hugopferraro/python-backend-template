from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.dependencies.mediator import get_mediator, get_user_repository
from src.api.v1.dependencies.oauth2 import login_required
from src.api.v1.schemas.user_schemas import UserDetailResponse
from src.application.behaviour.mediator import Mediator
from src.application.usecases.user.get_user_request import GetUserRequest
from src.domain.repositories.user_domain_repository import UserDomainRepository

router = APIRouter()


@router.get("/me", response_model=UserDetailResponse)
def get_me(
    current_user=Depends(login_required),
    mediator: Mediator = Depends(get_mediator),
    repository: UserDomainRepository = Depends(get_user_repository),
):
    result = mediator.send(GetUserRequest(identifier=current_user.identifier.value), repository=repository)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return result
