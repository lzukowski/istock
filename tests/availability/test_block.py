from datetime import datetime, timedelta

from pytest import fixture, mark
from pytest_bdd import scenario, given, when, then

from istock.availability import (
    MasterpieceId,
    VariantId,
    OwnerId,
    MasterpiecePermanentlyBlockedEvent,
)
from istock.availability.masterpiece import MasterpieceRepository


@fixture
def masterpiece_id():
    return MasterpieceId.new()


@fixture
def variant_id():
    return VariantId.new()


@fixture
def owner_id():
    return OwnerId.new()


@given('published masterpiece')
def published_masterpiece_id(
        masterpiece_id, availability, event_listener_cleanup,
):
    availability.register(masterpiece_id)
    event_listener_cleanup()
    return masterpiece_id


@fixture
def reserved_variant_id(
        availability, event_listener_cleanup, masterpiece_id, variant_id,
        owner_id,
):
    assert availability.reserve(masterpiece_id, variant_id, owner_id)
    event_listener_cleanup()
    return variant_id


@mark.usefixtures('reserved_variant_id')
@given('masterpiece was reserved')
def reserve_variant(reserved_variant_id):
    return reserved_variant_id


@fixture
def masterpiece_permanently_blocked(
        availability, masterpiece_id, variant_id, owner_id,
):
    return availability.block(masterpiece_id, variant_id, owner_id)


@mark.usesfixture('masterpiece_permanently_blocked')
@when('masterpiece was bought')
def block_masterpiece():
    pass


@then('masterpiece is reserved as permanent block')
def check_if_masterpiece_was_blocked(
        masterpiece_permanently_blocked, event_listener, masterpiece_id,
        owner_id,
):
    assert masterpiece_permanently_blocked
    assert event_listener.domain_event_was_emitted(
        MasterpiecePermanentlyBlockedEvent(masterpiece_id, owner_id),
    )


@scenario('block.feature', 'Buying masterpiece')
def test_permanent_block_when_masterpiece_was_bought():
    pass


@mark.usesfixture('masterpiece_permanently_blocked')
@when('buying not reserved masterpiece')
def block_not_reserved_masterpiece():
    pass


@then('not reserved masterpiece is reserved as permanent block')
def check_if_not_reserved_masterpiece_was_blocked(
        masterpiece_permanently_blocked, event_listener, masterpiece_id,
        owner_id,
):
    assert masterpiece_permanently_blocked
    assert event_listener.domain_event_was_emitted(
        MasterpiecePermanentlyBlockedEvent(masterpiece_id, owner_id),
    )


@scenario('block.feature', 'Buying not reserved masterpiece')
def test_buying_not_reserved_masterpiece():
    pass


@fixture
@when('other buyer wants to buy <variant> of masterpiece')
def blocking_masterpiece_reserved_by_other_buyer(
        variant, availability, masterpiece_id, reserved_variant_id,
):
    check_variant = (
        reserved_variant_id if variant == 'same variant' else VariantId.new()
    )
    return availability.block(masterpiece_id, check_variant, OwnerId.new())


@then('reservation is rejected')
def check_reservation_by_other_buyer(
        blocking_masterpiece_reserved_by_other_buyer,
):
    assert not blocking_masterpiece_reserved_by_other_buyer


@scenario('block.feature', 'Buying masterpiece reserved by other buyer')
def test_buying_masterpiece_already_reserved():
    pass


@given('masterpiece with expired reservation')
def expired_reserved_masterpiece_id(
        container, published_masterpiece_id, owner_id,
        event_listener_cleanup,
):
    masterpiece_repo = container.get(MasterpieceRepository)
    masterpiece = masterpiece_repo.get(published_masterpiece_id)
    masterpiece.reserve(
        VariantId.new(), owner_id, datetime.now() - timedelta(1),
    )
    event_listener_cleanup()
    return published_masterpiece_id


@when('other buyer wants to buy masterpiece')
def buying_masterpiece_with_expired_reservation(
        availability, expired_reserved_masterpiece_id,
):
    assert availability.block(
        expired_reserved_masterpiece_id, VariantId.new(), OwnerId.new(),
    )


@then('masterpiece is reserved as permanent block')
def check_if_reserved_masterpiece_was_blocked_by_new_user(event_listener):
    event_listener.domain_event_was_emitted(MasterpiecePermanentlyBlockedEvent)


@scenario('block.feature', 'Buying masterpiece which reservation expired')
def test_buying_masterpiece_with_expired_reservation():
    pass


@given('purchased masterpiece')
def purchased_masterpiece_id(availability, masterpiece_id, owner_id):
    assert availability.block(masterpiece_id, VariantId.new(), owner_id)
    return masterpiece_id


@fixture
@when('same buyer wants to <action> other variation of masterpiece')
def new_variation_blocking(
        action, availability, purchased_masterpiece_id, owner_id,
):
    return getattr(availability, action)(
        purchased_masterpiece_id, VariantId.new(), owner_id,
    )


@then('succeed with permanent variation block')
def check_buying_of_new_variation(new_variation_blocking):
    assert new_variation_blocking


@scenario(
    'block.feature', 'Buying other variation for already blocked masterpiece',
    example_converters={
        'action': {
            'reserve': 'reserve',
            'buy': 'block',
        }.get
    }
)
def test_buying_new_variation_of_blocked_masterpiece():
    pass
