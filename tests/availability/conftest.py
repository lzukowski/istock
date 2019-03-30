from typing import Dict

from injector import Injector
from pytest import fixture

from istock.availability import AvailabilityModule, MasterpieceId
from istock.availability.exceptions import AlreadyRegistered, NotFound
from istock.availability.masterpiece import MasterpieceRepository, Masterpiece


class InMemoryMasterpieceRepository(MasterpieceRepository):
    def __init__(self):
        self._masterpieces: Dict[MasterpieceId, Masterpiece] = {}

    def save(self, masterpiece: Masterpiece) -> None:
        in_repo = self._masterpieces.get(masterpiece.id)
        if in_repo and in_repo is not masterpiece:
            raise AlreadyRegistered(masterpiece.id)
        self._masterpieces[masterpiece.id] = masterpiece

    def get(self, masterpiece_id: MasterpieceId) -> Masterpiece:
        if masterpiece_id not in self._masterpieces:
            raise NotFound(masterpiece_id)
        return self._masterpieces[masterpiece_id]


@fixture
def container():
    container = Injector(AvailabilityModule)
    container.binder.bind(
        MasterpieceRepository, to=InMemoryMasterpieceRepository,
    )
    return container
