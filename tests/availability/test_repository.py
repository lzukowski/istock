from datetime import datetime, timedelta

from pytest import fixture, raises

from istock.availability import MasterpieceId, VariantId, OwnerId
from istock.availability.exceptions import NotFound
from istock.availability.masterpiece import Masterpiece, Reservation
from istock.availability.repository import MasterpieceSQLRepository


class TestMasterpieceMapper:
    def test_create_masterpiece_and_save(self, dbsession):
        masterpiece = Masterpiece(MasterpieceId.new())
        dbsession.add(masterpiece)
        dbsession.flush()

        assert dbsession.query(Masterpiece).one() == masterpiece

    def test_reservations_stored_with_masterpiece(self, dbsession):
        owner_id = OwnerId.new()
        reservations = [VariantId.new(), VariantId.new(), VariantId.new()]
        deadline = datetime.now() + timedelta(days=7)

        masterpiece = Masterpiece(MasterpieceId.new())
        for variant_id in reservations:
            masterpiece.reserve(variant_id, owner_id, deadline)

        dbsession.add(masterpiece)
        dbsession.flush()

        assert dbsession.query(Masterpiece).one() == masterpiece
        assert dbsession.query(Reservation).count() == len(reservations)

    def test_delete_all_when_deleting_masterpiece(self, dbsession):
        masterpiece = Masterpiece(MasterpieceId.new())
        owner_id = OwnerId.new()
        deadline = datetime.now() + timedelta(days=7)
        masterpiece.reserve(VariantId.new(), owner_id, deadline)
        masterpiece.reserve(VariantId.new(), owner_id, deadline)
        masterpiece.reserve(VariantId.new(), owner_id, deadline)

        dbsession.add(masterpiece)
        dbsession.flush()

        dbsession.delete(masterpiece)
        dbsession.flush()
        assert dbsession.query(Masterpiece).count() == 0
        assert dbsession.query(Reservation).count() == 0


class TestMasterpieceSQLRepository:
    @fixture
    def repository(self, container):
        return container.get(MasterpieceSQLRepository)

    def test_stores_masterpiece_on_save(self, repository, dbsession):
        masterpiece = Masterpiece(MasterpieceId.new())
        repository.save(masterpiece)
        assert dbsession.query(Masterpiece).count() == 1

    def test_updates_masterpiece_when_changed(self, repository, dbsession):
        masterpiece = Masterpiece(MasterpieceId.new())
        repository.save(masterpiece)

        assert dbsession.query(Masterpiece).one() == masterpiece

        owner_id = OwnerId.new()
        variant_id = VariantId.new()
        deadline = datetime.now() + timedelta(days=7)
        masterpiece.reserve(variant_id, owner_id, deadline)
        masterpiece.block(variant_id, owner_id)
        repository.save(masterpiece)

        assert dbsession.query(Masterpiece).one() == masterpiece
        assert dbsession.query(Reservation).count() != 0

    def test_emits_masterpiece_events_on_save(
            self, repository, event_listener,
    ):
        masterpiece = Masterpiece(MasterpieceId.new())
        masterpiece.reserve(VariantId.new(), OwnerId.new(), datetime.now())
        assert masterpiece.events_to_emit

        repository.save(masterpiece)

        assert event_listener.events
        for event in masterpiece.events_to_emit:
            assert event_listener.domain_event_was_emitted(event)

    def test_get_masterpiece_by_id(self, repository):
        masterpiece = Masterpiece(MasterpieceId.new())
        masterpiece.reserve(VariantId.new(), OwnerId.new(), datetime.now())
        repository.save(masterpiece)

        assert repository.get(masterpiece.id) == masterpiece

    def test_raises_when_no_masterpiece(self, repository):
        with raises(NotFound):
            repository.get(MasterpieceId.new())
