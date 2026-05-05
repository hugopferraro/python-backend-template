from typing import Generic, TypeVar

T = TypeVar("T")


class Request(Generic[T]):
    pass
