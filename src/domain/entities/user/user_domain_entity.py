from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.domain.exceptions.users.user_exception import UserException
from src.domain.vo.user import PersonalInfo, UserID, Email, HashedPassword

if TYPE_CHECKING:
    from src.domain.repositories.user_domain_repository import UserDomainRepository


@dataclass(frozen=True)
class UserDomainEntity:
    identifier: UserID
    personal_info: PersonalInfo
    email: Email
    hashed_password: HashedPassword

    @staticmethod
    def create(
            personal_info: PersonalInfo,
            email: Email,
            hashed_password: HashedPassword,
            user_domain_repository: UserDomainRepository,
    ) -> "UserDomainEntity":
        if user_domain_repository.find_by_email(email):
            raise UserException.user_already_exists()

        user = UserDomainEntity(
            identifier=UserID(),
            email=email,
            personal_info=personal_info,
            hashed_password=hashed_password,
        )

        user_domain_repository.save(user)

        return user