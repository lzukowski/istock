from abc import abstractmethod, ABCMeta
from copy import copy
from dataclasses import dataclass
from typing import List
from uuid import UUID


class MasterpieceId(UUID):
    pass


@dataclass(frozen=True)
class AvailabilityEvent:
    masterpiece_id: MasterpieceId


class AvailableEvent(AvailabilityEvent):
    pass


class Masterpiece:
    def __init__(self, masterpiece_id: MasterpieceId):
        self._id = masterpiece_id
        self._events: List[AvailabilityEvent] = []
        self._events.append(AvailableEvent(masterpiece_id))

    @property
    def id(self) -> MasterpieceId:
        return self._id

    @property
    def events_to_emit(self) -> List[AvailabilityEvent]:
        return copy(self._events)


class MasterpieceRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, masterpiece: Masterpiece) -> None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def get(
            self, masterpiece_id: MasterpieceId,
    ) -> Masterpiece:  # pragma: no cover
        raise NotImplementedError
