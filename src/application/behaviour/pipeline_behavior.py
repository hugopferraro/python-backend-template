from abc import ABC, abstractmethod
from typing import Callable, TypeVar

from src.application.behaviour.request import Request

T = TypeVar("T")


class PipelineBehavior(ABC):
    @abstractmethod
    def handle(self, request: Request, next: Callable[[], T]) -> T: ...
