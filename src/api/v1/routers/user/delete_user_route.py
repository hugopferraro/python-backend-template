from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.dependencies.mediator import get_mediator, get_user_repository
from src.api.v1.dependencies.oauth2 import login_required
from src.application.behaviour.mediator import Mediator
from src.application.usecases.user.delete_user_request import DeleteUserRequest
from src.domain.repositories.user_domain_repository import UserDomainRepository

router = APIRouter()


@router.delete("/{identifier}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    identifier: str,
    _=Depends(login_required),
    mediator: Mediator = Depends(get_mediator),
    repository: UserDomainRepository = Depends(get_user_repository),
):
    result = mediator.send(DeleteUserRequest(identifier=identifier), repository=repository)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
