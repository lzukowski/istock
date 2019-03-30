class AvailabilityError(Exception):
    pass


class AlreadyRegistered(AvailabilityError):
    pass


class NotFound(AvailabilityError):
    pass
