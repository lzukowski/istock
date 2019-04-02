from collections import deque
from datetime import datetime

from injector import inject
from sqlalchemy import Table, MetaData, Column, ForeignKey, DateTime, event
from sqlalchemy.orm import mapper, relationship, Session
from sqlalchemy.orm.query import QueryContext
from sqlalchemy_utils import UUIDType

from istock.availability import (
    MasterpieceId,
    AvailabilityEvent,
    AvailabilityListener,
)
from istock.availability.exceptions import NotFound
from istock.availability.masterpiece import (
    Reservation,
    Masterpiece,
    MasterpieceRepository,
)

metadata = MetaData()

masterpieces_table = Table(
    'masterpieces', metadata, Column('id', UUIDType, primary_key=True),
)
reservations_table = Table(
    'reservations',
    metadata,
    Column(
        'masterpiece_id',
        UUIDType,
        ForeignKey(masterpieces_table.c.id),
        primary_key=True,
    ),
    Column('variant_id', UUIDType, primary_key=True),
    Column('owner_id', UUIDType, primary_key=True),
    Column('deadline', DateTime, nullable=True, primary_key=True),
)

ReservationMapper = mapper(
    Reservation,
    reservations_table,
    properties={
        '_column_masterpiece_id': reservations_table.c.masterpiece_id,
        'variant_id': reservations_table.c.variant_id,
        'owner_id': reservations_table.c.owner_id,
        'deadline': reservations_table.c.deadline,
    },
)

MasterpieceMapper = mapper(
    Masterpiece,
    masterpieces_table,
    properties={
        '_id': masterpieces_table.c.id,
        '_reservations': relationship(
            ReservationMapper, lazy='joined', cascade='all, delete, merge',
        ),
    },
)


@event.listens_for(Masterpiece, 'load')
def receive_load_for_reservation(target: Masterpiece, _: QueryContext) -> None:
    target._events = deque()  # pylint: disable=protected-access


class MasterpieceSQLRepository(MasterpieceRepository):
    @inject
    def __init__(
            self, session: Session, listener: AvailabilityListener,
    ) -> None:
        self._session = session
        self._listener = listener

    def save(self, masterpiece: Masterpiece) -> None:
        self._session.add(masterpiece)
        self._session.flush()
        for e in masterpiece.events_to_emit:
            self._listener.emit(AvailabilityEvent(e, datetime.now()))

    def get(self, masterpiece_id: MasterpieceId) -> Masterpiece:
        masterpiece = self._session.query(Masterpiece).get(masterpiece_id)
        if not masterpiece:
            raise NotFound(masterpiece_id)
        return masterpiece
