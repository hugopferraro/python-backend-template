import inspect
from typing import TypeVar

from src.application.behaviour.handler_registry import _get_global_registry
from src.application.behaviour.pipeline_behavior import PipelineBehavior
from src.application.behaviour.request import Request

T = TypeVar("T")


class Mediator:
    def __init__(self, behaviors: list[PipelineBehavior] | None = None) -> None:
        self._behaviors = behaviors or []

    def send(self, request: Request[T], **dependencies) -> T:
        """
        Dispatch a request to its registered handler.

        Dependencies (e.g. repository) are passed separately from the request because
        handlers are stateless singletons — infrastructure dependencies like database
        sessions are per-request and cannot be injected at construction time.
        """
        handler = _get_global_registry().get(type(request))
        self._validate_dependencies(handler, dependencies)
        pipeline = lambda: handler.handle(request, **dependencies)

        for behavior in reversed(self._behaviors):
            current_next = pipeline
            pipeline = lambda b=behavior, n=current_next: b.handle(request, n)

        return pipeline()

    @staticmethod
    def _validate_dependencies(handler, dependencies: dict) -> None:
        sig = inspect.signature(handler.handle)
        for name, param in sig.parameters.items():
            if name in ("self", "request"):
                continue
            if param.default is param.empty and name not in dependencies:
                raise TypeError(
                    f"{type(handler).__name__}.handle() missing required dependency: '{name}'"
                )
