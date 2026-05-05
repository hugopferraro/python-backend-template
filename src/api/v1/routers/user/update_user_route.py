from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.dependencies.mediator import get_mediator, get_user_repository
from src.api.v1.dependencies.oauth2 import login_required
from src.api.v1.schemas.user_schemas import UserResponse, UserUpdateSchema
from src.application.behaviour.mediator import Mediator
from src.application.usecases.user.update_user_request import UpdateUserRequest
from src.domain.repositories.user_domain_repository import UserDomainRepository

router = APIRouter()


@router.put("/{identifier}", response_model=UserResponse)
def update(
    identifier: str,
    body: UserUpdateSchema,
    _=Depends(login_required),
    mediator: Mediator = Depends(get_mediator),
    repository: UserDomainRepository = Depends(get_user_repository),
):
    result = mediator.send(UpdateUserRequest(
        identifier=identifier,
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
    ), repository=repository)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return result
