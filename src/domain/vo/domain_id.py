import re
import secrets
import time
from dataclasses import dataclass
from typing import ClassVar, Pattern

from src.domain.exceptions.users.user_exception import UserException


@dataclass(frozen=True)
class DomainID:
    """
    Value Object representing a Domain Identifier.
    Uses a ULID-like format with Crockford's Base32 encoding.
    """

    _value: str

    ENCODING: ClassVar[str] = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
    MASK: ClassVar[int] = 0x1F
    MASK_BITS: ClassVar[int] = 5
    VALID_PATTERN: ClassVar[Pattern[str]] = re.compile(r"[0-9A-HJKMNP-TV-Z]{26}")

    def __post_init__(self) -> None:
        if self._value is None:
            raise ValueError("DomainID value cannot be null")

        if not self.is_valid(self._value):
            raise UserException.invalid_id()

    @staticmethod
    def of(value: str) -> "DomainID":
        return DomainID(value)

    @staticmethod
    def is_valid(value: str | None) -> bool:
        return value is not None and bool(DomainID.VALID_PATTERN.fullmatch(value))

    @staticmethod
    def generate() -> str:
        timestamp = int(time.time() * 1000)
        buffer = [""] * 26

        # timestamp: 48 bits -> 10 chars
        DomainID._write_base32(buffer, timestamp, 10, 0)

        # randomness: 80 bits -> 16 chars
        DomainID._write_base32(buffer, secrets.randbits(40), 8, 10)
        DomainID._write_base32(buffer, secrets.randbits(40), 8, 18)

        return "".join(buffer)

    @staticmethod
    def _write_base32(
        buffer: list[str],
        value: int,
        count: int,
        offset: int,
    ) -> None:
        for i in range(count):
            shift = (count - i - 1) * DomainID.MASK_BITS
            index = (value >> shift) & DomainID.MASK
            buffer[offset + i] = DomainID.ENCODING[index]

    @property
    def value(self) -> str:
        return self._value

    def get_value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value