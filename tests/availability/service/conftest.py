from injector import SingletonScope
from pytest import fixture

from istock.availability import AvailabilityService, AvailabilityListener
from tests.availability.conftest import QueueEventListener


@fixture
def availability(container):
    return container.get(AvailabilityService)


@fixture(autouse=True)
def event_listener(container):
    container.binder.bind(
        AvailabilityListener, to=QueueEventListener, scope=SingletonScope,
    )
    return container.get(AvailabilityListener)
