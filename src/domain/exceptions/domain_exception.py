from src.domain.exceptions.code.error_code import ErrorCode
from src.domain.exceptions.error_detail import ErrorDetail


class DomainException(RuntimeError):
    def __init__(self, error_code: ErrorCode, errors: list[ErrorDetail] | None = None):
        super().__init__(error_code.code())
        self._error_code = error_code
        self._errors = errors or []

    def error_code(self) -> ErrorCode:
        return self._error_code

    def errors(self) -> list[ErrorDetail]:
        return self._errors

    def add_error(self, field: str, message: str) -> None:
        self._errors.append(ErrorDetail(field, message))