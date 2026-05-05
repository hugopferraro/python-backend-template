from src.api.v1.schemas.user_schemas import UserDetailResponse
from src.application.behaviour.handler import Handler
from src.application.behaviour.handler_registry import use_case
from src.application.usecases.user.list_users_request import ListUsersRequest
from src.domain.repositories.user_domain_repository import UserDomainRepository


@use_case
class ListUsersUseCase(Handler[ListUsersRequest, list[UserDetailResponse]]):
    def handle(self, request: ListUsersRequest, *, repository: UserDomainRepository) -> list[UserDetailResponse]:
        dtos = repository.list(search=request.search)
        return [
            UserDetailResponse(
                id=dto.identifier.value,
                first_name=dto.personal_info.first_name,
                last_name=dto.personal_info.last_name,
                email=dto.email.value,
                created_at=dto.created_at,
                updated_at=dto.updated_at,
            )
            for dto in dtos
        ]
