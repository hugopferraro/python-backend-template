from src.api.v1.schemas.user_schemas import UserResponse
from src.application.behaviour.handler import Handler
from src.application.behaviour.handler_registry import use_case
from src.application.usecases.user.create_user_request import CreateUserRequest
from src.domain.entities.user.user_domain_entity import UserDomainEntity
from src.domain.repositories.user_domain_repository import UserDomainRepository
from src.domain.vo.user import PersonalInfo, Email, HashedPassword


@use_case
class CreateUserUseCase(Handler[CreateUserRequest, UserResponse]):
    def handle(self, request: CreateUserRequest, *, repository: UserDomainRepository) -> UserResponse:
        entity = UserDomainEntity.create(
            personal_info=PersonalInfo(
                first_name=request.first_name,
                last_name=request.last_name,
            ),
            email=Email(value=request.email),
            hashed_password=HashedPassword.create(request.password),
            user_domain_repository=repository,
        )
        return UserResponse(
            id=entity.identifier.value,
            first_name=entity.personal_info.first_name,
            last_name=entity.personal_info.last_name,
            email=entity.email.value,
        )
