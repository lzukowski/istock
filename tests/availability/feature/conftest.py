from collections import deque
from dataclasses import dataclass, field
from typing import Deque

from injector import SingletonScope
from pytest import fixture

from istock.availability import (
    AvailabilityService,
    AvailabilityListener,
    AvailabilityEvent,
    MasterpieceEvent,
)


@dataclass
class QueueEventListener(AvailabilityListener):
    events: Deque[AvailabilityEvent] = field(default_factory=deque)

    def emit(self, event: AvailabilityEvent) -> None:
        self.events.append(event)

    def reset(self) -> None:
        self.events = deque()

    def domain_event_was_emitted(self, event: MasterpieceEvent) -> bool:
        return any([e.payload == event for e in self.events])


@fixture
def availability(container):
    return container.get(AvailabilityService)


@fixture(autouse=True)
def event_listener(container):
    container.binder.bind(
        AvailabilityListener, to=QueueEventListener, scope=SingletonScope,
    )
    return container.get(AvailabilityListener)
