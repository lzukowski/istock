from uuid import uuid1
from pytest import fixture

from istock.availability import MasterpieceId
from istock.availability.masterpiece import MasterpieceRepository
from istock.availability.register import Register


class TestRegister:
    @fixture
    def register(self, masterpiece_repo):
        return Register(masterpiece_repo)

    @fixture
    def masterpiece_repo(self, container):
        return container.get(MasterpieceRepository)

    @fixture
    def masterpiece_id(self):
        return MasterpieceId(hex=uuid1().hex)

    def test_adds_masterpiece_when_registered(
            self, register, masterpiece_id, masterpiece_repo,
    ):
        register(masterpiece_id)
        assert masterpiece_repo.get(masterpiece_id) is not None
