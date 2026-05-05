from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.application.behaviour.request import Request

R = TypeVar("R", bound=Request)
T = TypeVar("T")


class Handler(ABC, Generic[R, T]):
    @abstractmethod
    def handle(self, request: R, **dependencies) -> T: ...
