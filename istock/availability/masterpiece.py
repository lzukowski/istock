from abc import ABCMeta, abstractmethod
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import List, Deque, TypeVar, Generic, Type, Optional
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
class MasterpieceBlockedEvent(MasterpieceEvent):
    owner_id: OwnerId


class MasterpiecePermanentlyBlockedEvent(MasterpieceBlockedEvent):
    pass


@dataclass(frozen=True)
class Reservation:
    variant_id: VariantId
    owner_id: OwnerId
    deadline: Optional[datetime]

    @property
    def active(self) -> bool:
        return self.permanent or datetime.now() < self.deadline

    @property
    def permanent(self) -> bool:
        return self.deadline is None

    def blocks(self, other: 'Reservation') -> bool:
        if not self.active:
            return False

        if other.owner_id != self.owner_id:
            return True

        if other.variant_id == self.variant_id:
            if self.permanent:
                return True

            if not other.permanent:
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
        self._events.append(MasterpieceBlockedEvent(self.id, owner_id))
        return True

    def block(self, variant_id: VariantId, owner_id: OwnerId) -> bool:
        reservation = Reservation(variant_id, owner_id, None)

        any_blockers = any([r.blocks(reservation) for r in self._reservations])
        if any_blockers:
            return False

        only_permanent_reservations = [
            r for r in self._reservations if r.permanent
        ]
        only_permanent_reservations.append(reservation)
        self._reservations = only_permanent_reservations

        self._events.append(
            MasterpiecePermanentlyBlockedEvent(self.id, owner_id),
        )
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
