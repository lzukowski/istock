from dataclasses import replace
from datetime import datetime, timedelta

from pytest import fixture

from istock.availability import MasterpieceAvailableEvent
from istock.availability.masterpiece import (
    MasterpieceId,
    VariantId,
    OwnerId,
    Reservation,
    Masterpiece,
    MasterpieceBlocked,
)


class TestReservation:
    @fixture
    def reservation(self):
        return Reservation(
            VariantId.new(), OwnerId.new(), datetime.now() + timedelta(1),
        )

    def test_in_force_when_deadline_not_passed(self, reservation):
        assert reservation.in_force is True

    def test_not_in_force_when_deadline_expires(self, reservation):
        reservation = replace(
            reservation, deadline=datetime.now() - timedelta(days=1),
        )
        assert reservation.in_force is False

    def test_blocks_when_same_variation_for_same_owner(self, reservation):
        other = replace(reservation, deadline=datetime.now() + timedelta(2))
        assert reservation.blocks(other) is True

    def test_blocks_when_other_owner(self, reservation):
        assert reservation.blocks(
            replace(reservation, owner_id=OwnerId.new())
        ) is True
        assert reservation.blocks(
            replace(
                reservation,
                owner_id=OwnerId.new(),
                variant_id=VariantId.new(),
            )
        ) is True

    def test_not_blocking_other_for_same_owner(self, reservation):
        assert reservation.blocks(
            replace(reservation, variant_id=VariantId.new())
        ) is False

    def test_not_blocking_when_deadline_passes(self, reservation):
        expired = replace(
            reservation, deadline=datetime.now() - timedelta(1),
        )

        assert expired.blocks(reservation) is False
        assert expired.blocks(
            replace(reservation, owner_id=OwnerId.new())
        ) is False


class TestMasterpieceCreation:
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
        return datetime.now() + timedelta(7)

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
        assert masterpiece.reserve(variant_id, owner_id, deadline) is False

    def test_fail_when_reserving_masterpiece_already_blocked_by_other_owner(
            self, masterpiece, variant_id, owner_id, deadline,
    ):
        assert masterpiece.reserve(variant_id, owner_id, deadline) is True

        assert masterpiece.reserve(
            variant_id, OwnerId.new(), deadline,
        ) is False
        assert masterpiece.reserve(
            variant_id, OwnerId.new(), deadline,
        ) is False
        assert masterpiece.reserve(
            VariantId.new(), OwnerId.new(), deadline,
        ) is False

    def test_succeed_when_reserving_masterpiece_with_expired_reservation(
            self, masterpiece, variant_id, owner_id, deadline,
    ):
        expired_deadline = datetime.now() - timedelta(1)
        assert masterpiece.reserve(variant_id, owner_id, expired_deadline)
        assert masterpiece.reserve(
            VariantId.new(), OwnerId.new(), deadline,
        ) is True
