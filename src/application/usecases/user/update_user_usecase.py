from src.api.v1.schemas.user_schemas import UserResponse
from src.application.behaviour.handler import Handler
from src.application.behaviour.handler_registry import use_case
from src.application.usecases.user.update_user_request import UpdateUserRequest
from src.domain.entities.user.user_domain_entity import UserDomainEntity
from src.domain.repositories.user_domain_repository import UserDomainRepository
from src.domain.vo.user import UserID, PersonalInfo, Email


@use_case
class UpdateUserUseCase(Handler[UpdateUserRequest, UserResponse | None]):
    def handle(self, request: UpdateUserRequest, *, repository: UserDomainRepository) -> UserResponse | None:
        dto = repository.find_by_identifier(UserID(value=request.identifier))
        if dto is None:
            return None

        updated_entity = UserDomainEntity(
            identifier=dto.identifier,
            personal_info=PersonalInfo(
                first_name=request.first_name or dto.personal_info.first_name,
                last_name=request.last_name or dto.personal_info.last_name,
            ),
            email=Email(value=request.email) if request.email is not None else dto.email,
            hashed_password=dto.hashed_password,
        )

        repository.save(updated_entity)

        return UserResponse(
            id=updated_entity.identifier.value,
            first_name=updated_entity.personal_info.first_name,
            last_name=updated_entity.personal_info.last_name,
            email=updated_entity.email.value,
        )
