from injector import Module, inject, Binder

from .events import (
    AvailabilityEvent,
    AvailabilityListener,
    NotEmittingListener,
)
from .masterpiece import (
    MasterpieceId,
    MasterpieceEvent,
    MasterpieceAvailableEvent,
)
from .register import Register


class AvailabilityService:
    register: Register

    @inject
    def __init__(self, register_service: Register) -> None:
        self.register = register_service


class AvailabilityModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(AvailabilityListener, to=NotEmittingListener)


__all__ = [
    'MasterpieceId',
    'AvailabilityListener',
    'AvailabilityEvent',
    'MasterpieceEvent',
    'MasterpieceAvailableEvent',
    'AvailabilityService',
    'AvailabilityModule',
]
