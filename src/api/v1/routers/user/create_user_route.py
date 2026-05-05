from fastapi import APIRouter, Depends

from src.api.v1.dependencies.mediator import get_mediator, get_user_repository
from src.api.v1.schemas.user_schemas import UserCreateSchema, UserResponse
from src.application.behaviour.mediator import Mediator
from src.application.usecases.user.create_user_request import CreateUserRequest
from src.domain.repositories.user_domain_repository import UserDomainRepository

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=201)
def create(
    body: UserCreateSchema,
    mediator: Mediator = Depends(get_mediator),
    repository: UserDomainRepository = Depends(get_user_repository),
):
    return mediator.send(CreateUserRequest(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        password=body.password,
    ), repository=repository)
