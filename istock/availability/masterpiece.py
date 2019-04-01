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
        return cls(hex=uuid1().hex)


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

    @property
    def in_force(self) -> bool:
        return datetime.now() < self.deadline

    def blocks(self, other: 'Reservation') -> bool:
        if not self.in_force:
            return False

        if other.owner_id != self.owner_id:
            return True

        if other.variant_id == self.variant_id:
            return True

        return False


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
        reservation = Reservation(variant_id, owner_id, deadline)
        any_blockers = any([r.blocks(reservation) for r in self._reservations])

        if any_blockers:
            return False

        self._reservations.append(reservation)
        self._events.append(MasterpieceBlocked(self.id, owner_id))
        return True


class MasterpieceRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, masterpiece: Masterpiece) -> None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def get(
            self, masterpiece_id: MasterpieceId,
    ) -> Masterpiece:  # pragma: no cover
        raise NotImplementedError
