from sqlalchemy import Table, MetaData, Column, ForeignKey, DateTime
from sqlalchemy.orm import mapper, relationship
from sqlalchemy_utils import UUIDType

from istock.availability.masterpiece import Reservation, Masterpiece

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
