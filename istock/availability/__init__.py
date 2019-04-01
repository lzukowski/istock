from datetime import timedelta, datetime

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


class ReservationPeriod(timedelta):
    pass


class AvailabilityService:
    @inject
    def __init__(
            self,
            reservation_period: ReservationPeriod,
            masterpiece_repo: MasterpieceRepository,
    ) -> None:
        self._repo = masterpiece_repo
        self._reservation_period = reservation_period

    def register(self, masterpiece_id: MasterpieceId) -> None:
        mp = Masterpiece(masterpiece_id)
        self._repo.save(mp)

    def reserve(
            self,
            masterpiece_id: MasterpieceId,
            variant_id: VariantId,
            owner_id: OwnerId,
    ) -> bool:
        mp = self._repo.get(masterpiece_id)
        deadline = datetime.now() + self._reservation_period
        if not mp.reserve(variant_id, owner_id, deadline):
            return False
        self._repo.save(mp)
        return True


class AvailabilityModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(AvailabilityListener, to=NotEmittingListener)
        binder.bind(ReservationPeriod, to=ReservationPeriod(days=7))


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
