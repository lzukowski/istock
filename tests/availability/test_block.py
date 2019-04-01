from pytest import fixture, mark
from pytest_bdd import scenario, given, when, then

from istock.availability import (
    MasterpieceId,
    VariantId,
    OwnerId,
    MasterpiecePermanentlyBlockedEvent,
)


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


@given('masterpiece was reserved')
def reserve_variant_id(
        availability, event_listener_cleanup, masterpiece_id, variant_id,
        owner_id,
):
    assert availability.reserve(masterpiece_id, variant_id, owner_id)
    event_listener_cleanup()
    return variant_id


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
