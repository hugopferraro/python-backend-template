from dataclasses import dataclass
from datetime import datetime

from src.domain.vo.user import UserID, PersonalInfo, Email, HashedPassword


@dataclass(frozen=True)
class UserReadDTO:
    identifier: UserID
    personal_info: PersonalInfo
    email: Email
    hashed_password: HashedPassword
    created_at: datetime | None
    updated_at: datetime | None
