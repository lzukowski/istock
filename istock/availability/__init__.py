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
    Masterpiece,
    MasterpieceEvent,
    MasterpieceAvailableEvent,
    MasterpieceBlocked,
    MasterpieceRepository,
)


class AvailabilityService:
    @inject
    def __init__(self, masterpiece_repo: MasterpieceRepository) -> None:
        self._repo = masterpiece_repo

    def register(self, masterpiece_id: MasterpieceId) -> None:
        mp = Masterpiece(masterpiece_id)
        self._repo.save(mp)

    def reserve(
            self,
            masterpiece_id: MasterpieceId,
            variant_id: VariantId,
            owner_id: OwnerId,
    ) -> bool:
        raise NotImplementedError


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
