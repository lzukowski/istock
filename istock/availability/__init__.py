from injector import Module, inject

from .masterpiece import MasterpieceId
from .register import Register


class AvailabilityService:
    register: Register

    @inject
    def __init__(self, register_service: Register) -> None:
        self.register = register_service


class AvailabilityModule(Module):
    pass


__all__ = [
    'MasterpieceId',
    'AvailabilityService',
    'AvailabilityModule',
]
