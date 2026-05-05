from src.api.v1.schemas.user_schemas import UserDetailResponse
from src.application.behaviour.handler import Handler
from src.application.behaviour.handler_registry import use_case
from src.application.usecases.user.get_user_request import GetUserRequest
from src.domain.repositories.user_domain_repository import UserDomainRepository
from src.domain.vo.user import UserID


@use_case
class GetUserUseCase(Handler[GetUserRequest, UserDetailResponse | None]):
    def handle(self, request: GetUserRequest, *, repository: UserDomainRepository) -> UserDetailResponse | None:
        dto = repository.find_by_identifier(UserID(value=request.identifier))
        if dto is None:
            return None
        return UserDetailResponse(
            id=dto.identifier.value,
            first_name=dto.personal_info.first_name,
            last_name=dto.personal_info.last_name,
            email=dto.email.value,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
