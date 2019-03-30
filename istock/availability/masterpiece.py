from abc import ABCMeta, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import List, Deque
from uuid import UUID


class MasterpieceId(UUID):
    pass


class VariantId(UUID):
    pass


class OwnerId(UUID):
    pass


@dataclass(frozen=True)
class MasterpieceEvent:
    masterpiece_id: MasterpieceId


class MasterpieceAvailableEvent(MasterpieceEvent):
    pass


@dataclass(frozen=True)
class MasterpieceBlocked(MasterpieceEvent):
    owner_id: OwnerId


class Masterpiece:
    def __init__(self, masterpiece_id: MasterpieceId):
        self._id = masterpiece_id
        self._events: Deque[MasterpieceEvent] = deque()
        self._events.append(MasterpieceAvailableEvent(masterpiece_id))

    @property
    def id(self) -> MasterpieceId:
        return self._id

    @property
    def events_to_emit(self) -> List[MasterpieceEvent]:
        return list(self._events)


class MasterpieceRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, masterpiece: Masterpiece) -> None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def get(
            self, masterpiece_id: MasterpieceId,
    ) -> Masterpiece:  # pragma: no cover
        raise NotImplementedError
