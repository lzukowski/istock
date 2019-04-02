from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from typing import Dict, Deque

from injector import Injector, SingletonScope, inject
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.pool import QueuePool

from istock.availability import (
    MasterpieceId,
    AvailabilityService,
    AvailabilityModule,
    AvailabilityListener,
    AvailabilityEvent,
    MasterpieceEvent,
)
from istock.availability.exceptions import AlreadyRegistered, NotFound
from istock.availability.masterpiece import Masterpiece, MasterpieceRepository
from istock.availability.repository import metadata


class InMemoryMasterpieceRepository(MasterpieceRepository):
    @inject
    def __init__(self, listener: AvailabilityListener):
        self._listener = listener
        self._masterpieces: Dict[MasterpieceId, Masterpiece] = {}

    def save(self, masterpiece: Masterpiece) -> None:
        in_repo = self._masterpieces.get(masterpiece.id)
        if in_repo and in_repo is not masterpiece:
            raise AlreadyRegistered(masterpiece.id)
        self._masterpieces[masterpiece.id] = masterpiece
        for event in masterpiece.events_to_emit:
            self._listener.emit(AvailabilityEvent(event, datetime.now()))

    def get(self, masterpiece_id: MasterpieceId) -> Masterpiece:
        if masterpiece_id not in self._masterpieces:
            raise NotFound(masterpiece_id)
        return self._masterpieces[masterpiece_id]


@dataclass
class QueueEventListener(AvailabilityListener):
    events: Deque[AvailabilityEvent] = field(default_factory=deque)

    def emit(self, event: AvailabilityEvent) -> None:
        self.events.append(event)

    def reset(self) -> None:
        self.events = deque()

    def domain_event_was_emitted(self, event: MasterpieceEvent) -> bool:
        return any([e.payload == event for e in self.events])


@fixture(scope='session')
def dbsession_global():
    def _expire_all_session_wrapper(session, func):
        @wraps(func)
        def _wraps(*args, **kwargs):
            ret = func(*args, **kwargs)
            session.expire_all()
            return ret
        return _wraps

    engine = create_engine(
        'sqlite:///:memory:', poolclass=QueuePool, echo=False,
    )
    metadata.create_all(engine)

    dbsession = scoped_session(
        sessionmaker(bind=engine, autoflush=False, autocommit=False)
    )
    dbsession.flush = _expire_all_session_wrapper(dbsession, dbsession.flush)
    return dbsession


@fixture(scope='function')
def dbsession(dbsession_global):
    yield dbsession_global
    dbsession_global.flush()
    dbsession_global.rollback()


@fixture
def container(dbsession):
    container = Injector(AvailabilityModule)
    container.binder.bind(
        MasterpieceRepository,
        to=InMemoryMasterpieceRepository,
        scope=SingletonScope,
    )
    container.binder.bind(
        AvailabilityListener, to=QueueEventListener, scope=SingletonScope,
    )
    container.binder.bind(Session, to=dbsession)
    return container


@fixture
def availability(container):
    return container.get(AvailabilityService)


@fixture
def event_listener(container):
    return container.get(AvailabilityListener)


@fixture(autouse=True)
def event_listener_cleanup(event_listener):
    event_listener.reset()
    return event_listener.reset
