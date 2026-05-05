from typing import Callable, TypeVar

from src.application.behaviour.pipeline_behavior import PipelineBehavior
from src.application.behaviour.request import Request
from src.domain.exceptions.domain_exception import DomainException

T = TypeVar("T")


class ExceptionHandlingBehavior(PipelineBehavior):
    def handle(self, request: Request, next: Callable[[], T]) -> T:
        try:
            return next()
        except DomainException:
            raise
        except Exception as exc:
            raise RuntimeError("An unexpected error occurred") from exc
