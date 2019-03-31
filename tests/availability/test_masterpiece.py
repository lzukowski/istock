from datetime import datetime

from pytest import fixture

from istock.availability import MasterpieceAvailableEvent
from istock.availability.masterpiece import (
    MasterpieceId, VariantId, OwnerId, Masterpiece, MasterpieceBlocked,
)


class TestMasterpiece:
    @fixture
    def masterpiece_id(self):
        return MasterpieceId.new()

    def test_emits_availability_event_when_created(self, masterpiece_id):
        masterpiece = Masterpiece(masterpiece_id)
        assert masterpiece.events_to_emit == [
            MasterpieceAvailableEvent(masterpiece_id)
        ]


class TestMasterpieceReservation:
    @fixture
    def masterpiece(self):
        return Masterpiece(MasterpieceId.new())

    @fixture
    def variant_id(self):
        return VariantId.new()

    @fixture
    def owner_id(self):
        return OwnerId.new()

    @fixture
    def deadline(self):
        return datetime.now()

    def test_blocked_when_reserving(
            self, masterpiece, variant_id, owner_id, deadline,
    ):
        assert masterpiece.reserve(variant_id, owner_id, deadline) is True
        block_event = MasterpieceBlocked(masterpiece.id, owner_id)
        assert block_event in masterpiece.events_to_emit

    def test_fail_when_reserving_same_variation_second_time(
            self, masterpiece, variant_id, owner_id, deadline,
    ):
        assert masterpiece.reserve(variant_id, owner_id, deadline) is True

        assert masterpiece.reserve(
            variant_id, owner_id, datetime.now()
        ) is False

    def test_fail_when_reserving_masterpiece_already_blocked_by_other_owner(
            self, masterpiece, variant_id, owner_id, deadline,
    ):
        assert masterpiece.reserve(variant_id, owner_id, deadline) is True

        assert masterpiece.reserve(
            variant_id, OwnerId.new(), datetime.now(),
        ) is False
        assert masterpiece.reserve(
            variant_id, OwnerId.new(), datetime.now(),
        ) is False
        assert masterpiece.reserve(
            VariantId.new(), OwnerId.new(), datetime.now(),
        ) is False
