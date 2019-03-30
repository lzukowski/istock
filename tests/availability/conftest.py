from datetime import datetime
from typing import Dict
from uuid import uuid1

from injector import Injector, SingletonScope, inject
from pytest import fixture

from istock.availability import (
    AvailabilityModule,
    AvailabilityListener,
    MasterpieceId,
    VariantId,
    OwnerId,
    AvailabilityEvent,
)
from istock.availability.exceptions import AlreadyRegistered, NotFound
from istock.availability.masterpiece import Masterpiece, MasterpieceRepository


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


@fixture
def container():
    container = Injector(AvailabilityModule)
    container.binder.bind(
        MasterpieceRepository,
        to=InMemoryMasterpieceRepository,
        scope=SingletonScope,
    )
    return container


@fixture
def new_masterpiece_id():
    yield MasterpieceId(hex=uuid1().hex)


@fixture
def new_variant_id():
    yield VariantId(hex=uuid1().hex)


@fixture
def new_owner_id():
    yield OwnerId(hex=uuid1().hex)
