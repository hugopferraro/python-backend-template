from src.domain.exceptions.code.user_error_code import UserErrorCode
from src.domain.exceptions.domain_exception import DomainException


class UserException(DomainException):
    def __init__(self, code: UserErrorCode):
        super().__init__(code)

    @staticmethod
    def invalid_id() -> "UserException":
        return UserException(UserErrorCode.INVALID_ID)

    @staticmethod
    def invalid_email() -> "UserException":
        return UserException(UserErrorCode.INVALID_EMAIL)

    @staticmethod
    def invalid_token() -> "UserException":
        return UserException(UserErrorCode.INVALID_TOKEN)

    @staticmethod
    def invalid_personal_data(field: str, message: str) -> "UserException":
        exception = UserException(UserErrorCode.INVALID_PERSONAL_DATA)
        exception.add_error(field, message)
        return exception

    @staticmethod
    def user_already_exists() -> "UserException":
        return UserException(UserErrorCode.ALREADY_EXISTS)