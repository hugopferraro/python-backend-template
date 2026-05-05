from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from src.api.v1.dependencies.mediator import get_user_repository
from src.domain.entities.user.user_domain_entity import UserDomainEntity
from src.domain.repositories.user_domain_repository import UserDomainRepository
from src.domain.vo.user import UserID
from src.infrastructure.security.jwt import decode_access_token

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    repository: UserDomainRepository = Depends(get_user_repository),
) -> UserDomainEntity:
    payload = decode_access_token(token)

    user_id_str: str | None = payload.get("id")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = repository.find_by_identifier(UserID(value=user_id_str))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def login_required(user: UserDomainEntity = Depends(get_current_user)) -> UserDomainEntity:
    return user
