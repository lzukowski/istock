from collections import deque
from dataclasses import dataclass, field
from functools import wraps
from typing import Deque

from injector import Injector, SingletonScope
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.pool import QueuePool

from istock.availability import (
    AvailabilityService,
    AvailabilityModule,
    AvailabilityListener,
    AvailabilityEvent,
    MasterpieceEvent,
)
from istock.availability.masterpiece import MasterpieceRepository
from istock.availability.repository import metadata, MasterpieceSQLRepository


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
        to=MasterpieceSQLRepository,
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
