from dataclasses import dataclass

from src.domain.vo.domain_id import DomainID


@dataclass(frozen=True)
class UserID:
    value: str

    def __init__(self, value: str | None = None):
        object.__setattr__(
            self,
            "value",
            value if value is not None else DomainID.generate()
        )