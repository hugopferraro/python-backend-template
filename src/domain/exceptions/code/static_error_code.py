from dataclasses import dataclass


@dataclass(frozen=True)
class StaticErrorCode:
    value: str
    status: int = 400

    def code(self) -> str:
        return self.value

    def http_status(self) -> int:
        return self.status