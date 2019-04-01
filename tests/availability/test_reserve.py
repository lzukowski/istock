from datetime import datetime, timedelta

from pytest import fixture
from pytest_bdd import scenario, given, when, then

from istock.availability import (
    OwnerId,
    VariantId,
    MasterpieceId,
    MasterpieceBlockedEvent,
)
from istock.availability.masterpiece import Masterpiece, MasterpieceRepository


@fixture
def owner_id():
    return OwnerId.new()


@fixture
def variant_id():
    return VariantId.new()


@fixture
def masterpiece_id():
    return MasterpieceId.new()


@given('published masterpiece')
def published_masterpiece_id(masterpiece_id, availability):
    availability.register(masterpiece_id)
    return masterpiece_id


@when('customer reserve variant of masterpiece')
def reserve_variant_of_masterpiece(
        availability, masterpiece_id, variant_id, owner_id,
):
    assert availability.reserve(masterpiece_id, variant_id, owner_id)


@then('masterpiece is reserved')
def check_reserved_event(event_listener, masterpiece_id, owner_id):
    assert event_listener.domain_event_was_emitted(
        MasterpieceBlockedEvent(masterpiece_id, owner_id)
    )


@scenario('reserve.feature', 'Reserving masterpiece')
def test_reserving_masterpiece():
    pass


@given('reserved masterpiece variant')
def reserved_masterpiece_id(
        availability, published_masterpiece_id, variant_id, owner_id,
):
    availability.reserve(published_masterpiece_id, variant_id, owner_id)
    return published_masterpiece_id


@fixture
@when('owner reserve variant of masterpiece for second time')
def reserved_for_second_time(
        availability, reserved_masterpiece_id, variant_id, owner_id,
):
    return availability.reserve(reserved_masterpiece_id, variant_id, owner_id)


@then('reservation is rejected')
def check_second_reservation(reserved_for_second_time):
    assert not reserved_for_second_time


@scenario('reserve.feature', 'Reserving masterpiece variant for second time')
def test_second_reservation_of_variant():
    pass


@fixture
@when('owner reserve other variant of masterpiece')
def other_variant_reserved(availability, reserved_masterpiece_id, owner_id):
    return availability.reserve(
        reserved_masterpiece_id, VariantId.new(), owner_id,
    )


@then('variant is reserved')
def check_reservation_of_other_variant(other_variant_reserved):
    assert other_variant_reserved


@scenario(
    'reserve.feature',
    'Reserving masterpiece variant when other variation was already reserved',
)
def test_reserving_variant_when_other_customer_reserved_other_variant():
    pass


@fixture
@when('other buyer reserve other variant of masterpiece')
def reserve_variant_by_other_buyer(availability, reserved_masterpiece_id):
    return availability.reserve(
        reserved_masterpiece_id, VariantId.new(), OwnerId.new(),
    )


@then('reservation is rejected')
def check_reservation_by_other_buyer(reserve_variant_by_other_buyer):
    assert not reserve_variant_by_other_buyer


@scenario('reserve.feature', 'Reserving blocked masterpiece by other buyer')
def test_reserving_masterpiece_by_other_buyer():
    pass


@given('expired masterpiece variant reservation')
def expired_reservation_masterpiece_id(
        container, event_listener_cleanup, masterpiece_id,
):
    masterpiece = Masterpiece(masterpiece_id)
    masterpiece.reserve(
        VariantId.new(),
        OwnerId.new(),
        deadline=datetime.now() - timedelta(days=3),
    )

    container.get(MasterpieceRepository).save(masterpiece)
    event_listener_cleanup()
    return masterpiece_id


@scenario(
    'reserve.feature',
    'Reserving masterpiece variant when previous reservation expires',
)
def test_reserving_masterpiece_when_no_active_reservations():
    pass
