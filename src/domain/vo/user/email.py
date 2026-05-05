import re
from dataclasses import dataclass
from typing import ClassVar, Pattern

from src.domain.exceptions.users.user_exception import UserException


@dataclass(frozen=True)
class Email:
    value: str

    EMAIL_PATTERN: ClassVar[Pattern[str]] = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )

    def __post_init__(self) -> None:
        if not self.valid(self.value):
            raise UserException.invalid_email()

    @staticmethod
    def valid(value: str | None) -> bool:
        if value is None:
            return False

        return Email.EMAIL_PATTERN.fullmatch(value) is not None
