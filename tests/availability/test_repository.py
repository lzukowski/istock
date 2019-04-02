from datetime import datetime, timedelta

from istock.availability.masterpiece import (
    MasterpieceId,
    VariantId,
    OwnerId,
    Masterpiece,
    Reservation,
)


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
