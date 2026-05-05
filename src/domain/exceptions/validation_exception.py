from src.domain.exceptions.code.static_error_code import StaticErrorCode
from src.domain.exceptions.domain_exception import DomainException


class ValidationException(DomainException):
    def __init__(self):
        super().__init__(StaticErrorCode("VALIDATION_ERROR"))

    @staticmethod
    def create() -> "ValidationException":
        return ValidationException()