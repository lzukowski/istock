from uuid import uuid1

from pytest import fixture, mark
from pytest_bdd import given, when, then, scenario

from istock.availability import MasterpieceId, AvailabilityService


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
def check_masterpiece_availability():
    assert False


@mark.xfail(reason='Not implemented yet')
@scenario('availability.feature', 'Registering masterpiece')
def test_registering_masterpiece():
    pass
