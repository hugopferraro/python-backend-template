from enum import Enum


class UserErrorCode(Enum):
    INVALID_ID            = ("USER_INVALID_ID",            400)
    INVALID_EMAIL         = ("USER_INVALID_EMAIL",         400)
    INVALID_TOKEN         = ("USER_INVALID_TOKEN",         401)
    INVALID_PERSONAL_DATA = ("USER_INVALID_PERSONAL_DATA", 422)
    ALREADY_EXISTS        = ("USER_ALREADY_EXISTS",        409)
    NOT_FOUND             = ("USER_NOT_FOUND",             404)

    def __new__(cls, code: str, status: int):
        obj = object.__new__(cls)
        obj._value_ = code
        obj._status = status
        return obj

    def code(self) -> str:
        return self.value

    def http_status(self) -> int:
        return self._status