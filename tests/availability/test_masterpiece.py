from pytest import fixture

from istock.availability import MasterpieceAvailableEvent
from istock.availability.masterpiece import Masterpiece


class TestMasterpiece:
    @fixture
    def masterpiece_id(self, new_masterpiece_id):
        return new_masterpiece_id

    def test_emits_availability_event_when_created(self, masterpiece_id):
        masterpiece = Masterpiece(masterpiece_id)
        assert masterpiece.events_to_emit == [
            MasterpieceAvailableEvent(masterpiece_id)
        ]
