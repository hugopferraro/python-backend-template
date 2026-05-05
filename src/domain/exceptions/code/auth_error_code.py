from enum import Enum


class AuthErrorCode(Enum):
    INVALID_CREDENTIALS = ("AUTH_INVALID_CREDENTIALS", 401)

    def __new__(cls, code: str, status: int):
        obj = object.__new__(cls)
        obj._value_ = code
        obj._status = status
        return obj

    def code(self) -> str:
        return self.value

    def http_status(self) -> int:
        return self._status
