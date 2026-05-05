from src.api.v1.schemas.user_schemas import UserResponse
from src.application.behaviour.handler import Handler
from src.application.behaviour.handler_registry import use_case
from src.application.usecases.user.delete_user_request import DeleteUserRequest
from src.domain.repositories.user_domain_repository import UserDomainRepository
from src.domain.vo.user import UserID


@use_case
class DeleteUserUseCase(Handler[DeleteUserRequest, UserResponse | None]):
    def handle(self, request: DeleteUserRequest, *, repository: UserDomainRepository) -> UserResponse | None:
        entity = repository.delete(UserID(value=request.identifier))
        if entity is None:
            return None
        return UserResponse(
            id=entity.identifier.value,
            first_name=entity.personal_info.first_name,
            last_name=entity.personal_info.last_name,
            email=entity.email,
        )
