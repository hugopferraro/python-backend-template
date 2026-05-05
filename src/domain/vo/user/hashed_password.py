from dataclasses import dataclass

from passlib.context import CryptContext

_bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(frozen=True)
class HashedPassword:
    value: str

    def verify(self, plain: str) -> bool:
        return _bcrypt_context.verify(plain, self.value)

    @staticmethod
    def create(plain: str) -> "HashedPassword":
        return HashedPassword(value=_bcrypt_context.hash(plain))
