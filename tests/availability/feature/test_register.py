from uuid import uuid1

from pytest_bdd import given, when, then, scenario

from istock.availability import MasterpieceId, MasterpieceAvailableEvent


@given('masterpiece')
def masterpiece_id():
    return MasterpieceId(uuid1().hex)


@when('merchant is publishing masterpiece')
def register_masterpiece(availability):
    availability.register(masterpiece_id)


@then('masterpiece is available')
def check_masterpiece_availability(event_listener):
    assert any(
        [
            isinstance(e.payload, MasterpieceAvailableEvent)
            for e in event_listener.events
        ]
    )


@scenario('register.feature', 'Registering masterpiece')
def test_registering_masterpiece():
    pass
