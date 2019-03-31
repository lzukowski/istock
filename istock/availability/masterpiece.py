from abc import ABCMeta, abstractmethod
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import List, Deque, TypeVar, Generic, Type
from uuid import UUID, uuid1


T = TypeVar('T')


class InternalId(UUID, Generic[T]):
    @classmethod
    def new(cls: Type[T]) -> T:
        return uuid1()


class MasterpieceId(InternalId):
    pass


class VariantId(InternalId):
    pass


class OwnerId(InternalId):
    pass


@dataclass(frozen=True)
class MasterpieceEvent:
    masterpiece_id: MasterpieceId


class MasterpieceAvailableEvent(MasterpieceEvent):
    pass


@dataclass(frozen=True)
class MasterpieceBlocked(MasterpieceEvent):
    owner_id: OwnerId


@dataclass(frozen=True)
class Reservation:
    variant_id: VariantId
    owner_id: OwnerId
    deadline: datetime


class Masterpiece:
    _id: MasterpieceId
    _reservations: List[Reservation]

    def __init__(self, masterpiece_id: MasterpieceId):
        self._id = masterpiece_id
        self._events: Deque[MasterpieceEvent] = deque()
        self._events.append(MasterpieceAvailableEvent(masterpiece_id))
        self._reservations = []

    @property
    def id(self) -> MasterpieceId:
        return self._id

    @property
    def events_to_emit(self) -> List[MasterpieceEvent]:
        return list(self._events)

    def reserve(
            self,
            variant_id: VariantId,
            owner_id: OwnerId,
            deadline: datetime,
    ) -> bool:
        if self._is_masterpiece_reserved_for_other_merchant(owner_id):
            return False

        if self._is_variant_already_reserved(variant_id):
            return False

        self._reservations.append(Reservation(variant_id, owner_id, deadline))
        self._events.append(MasterpieceBlocked(self.id, owner_id))
        return True

    def _is_variant_already_reserved(self, variant_id: VariantId) -> bool:
        return any([r.variant_id == variant_id for r in self._reservations])

    def _is_masterpiece_reserved_for_other_merchant(self, owner_id) -> bool:
        return any([r.owner_id != owner_id for r in self._reservations])


class MasterpieceRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, masterpiece: Masterpiece) -> None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def get(
            self, masterpiece_id: MasterpieceId,
    ) -> Masterpiece:  # pragma: no cover
        raise NotImplementedError
