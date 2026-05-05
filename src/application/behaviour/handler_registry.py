import typing

from src.application.behaviour.handler import Handler

_global_registry: "HandlerRegistry | None" = None


def _get_global_registry() -> "HandlerRegistry":
    global _global_registry
    if _global_registry is None:
        _global_registry = HandlerRegistry()
    return _global_registry


def use_case(cls):
    for base in getattr(cls, "__orig_bases__", []):
        origin = typing.get_origin(base)
        if origin is not None:
            args = typing.get_args(base)
            if len(args) >= 2:
                _get_global_registry().register(args[0], cls())
                return cls
    raise TypeError(f"@use_case: {cls.__name__} must extend Handler[RequestType, ResponseType]")


class HandlerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[type, Handler] = {}

    def register(self, request_type: type, handler: Handler) -> None:
        self._handlers[request_type] = handler

    def get(self, request_type: type) -> Handler:
        handler = self._handlers.get(request_type)
        if handler is None:
            raise KeyError(f"No handler registered for {request_type.__name__}")
        return handler
