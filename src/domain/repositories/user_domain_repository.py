from typing import Protocol, TYPE_CHECKING

from src.domain.entities.user.user_domain_entity import UserDomainEntity
from src.domain.vo.user import UserID, Email

if TYPE_CHECKING:
    from src.application.usecases.user.user_read_dto import UserReadDTO


class UserDomainRepository(Protocol):
    def find_by_identifier(self, identifier: UserID) -> "UserReadDTO | None": ...

    def find_by_email(self, email: Email) -> UserDomainEntity | None: ...

    def list(self, search: str | None = None) -> "list[UserReadDTO]": ...

    def save(self, user: UserDomainEntity) -> None: ...

    def delete(self, identifier: UserID) -> UserDomainEntity | None: ...
