from injector import Injector
from pytest import fixture

from istock.availability import AvailabilityModule


@fixture
def container():
    return Injector(AvailabilityModule)
