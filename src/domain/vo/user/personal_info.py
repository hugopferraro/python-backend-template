from dataclasses import dataclass

from src.domain.exceptions.users.user_exception import UserException


@dataclass(frozen=True)
class PersonalInfo:
    first_name: str
    last_name: str

    def __post_init__(self) -> None:
        if self.first_name is None or self.first_name.strip() == "":
            raise UserException.invalid_personal_data(
                "first_name",
                "First name cannot be empty"
            )

        if self.last_name is None or self.last_name.strip() == "":
            raise UserException.invalid_personal_data(
                "last_name",
                "Last name cannot be empty"
            )