from src.domain.exceptions.code.auth_error_code import AuthErrorCode
from src.domain.exceptions.domain_exception import DomainException


class AuthException(DomainException):
    def __init__(self, code: AuthErrorCode):
        super().__init__(code)

    @staticmethod
    def invalid_credentials() -> "AuthException":
        return AuthException(AuthErrorCode.INVALID_CREDENTIALS)
