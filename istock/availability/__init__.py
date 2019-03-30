from injector import Module, inject, Binder

from .events import (
    AvailabilityEvent,
    AvailabilityListener,
    NotEmittingListener,
)
from .masterpiece import (
    MasterpieceId,
    VariantId,
    OwnerId,
    MasterpieceEvent,
    MasterpieceAvailableEvent,
    MasterpieceBlocked,
)
from .register import Register
from .reserve import Reserve


class AvailabilityService:
    register: Register
    reserve: Reserve

    @inject
    def __init__(
            self,
            register_service: Register,
            reserve_service: Reserve,
    ) -> None:
        self.register = register_service
        self.reserve = reserve_service


class AvailabilityModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(AvailabilityListener, to=NotEmittingListener)


__all__ = [
    'MasterpieceId',
    'VariantId',
    'OwnerId',
    'AvailabilityListener',
    'AvailabilityEvent',
    'MasterpieceEvent',
    'MasterpieceBlocked',
    'MasterpieceAvailableEvent',
    'AvailabilityService',
    'AvailabilityModule',
]
