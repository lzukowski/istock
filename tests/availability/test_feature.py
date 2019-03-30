from uuid import uuid1

from injector import SingletonScope
from pytest import fixture
from pytest_bdd import given, when, then, scenario

from istock.availability import (
    MasterpieceId,
    AvailabilityService,
    AvailabilityListener,
    MasterpieceAvailableEvent,
)
from .conftest import QueueEventListener


@fixture(autouse=True)
def event_listener(container):
    container.binder.bind(
        AvailabilityListener, to=QueueEventListener, scope=SingletonScope,
    )
    return container.get(AvailabilityListener)


@fixture
def availability(container):
    return container.get(AvailabilityService)


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


@scenario('availability.feature', 'Registering masterpiece')
def test_registering_masterpiece():
    pass
