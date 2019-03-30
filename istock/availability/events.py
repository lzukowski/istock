from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Union

from .masterpiece import MasterpieceEvent


@dataclass(frozen=True)
class AvailabilityEvent:
    payload: Union[MasterpieceEvent]
    created_at: datetime


class AvailabilityListener(metaclass=ABCMeta):
    @abstractmethod
    def emit(self, event: AvailabilityEvent) -> None:  # pragma: no cover
        raise NotImplementedError


class NotEmittingListener(AvailabilityListener):
    def emit(self, event: AvailabilityEvent) -> None:
        pass
