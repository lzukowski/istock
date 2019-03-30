from abc import abstractmethod
from uuid import UUID


class MasterpieceId(UUID):
    pass


class Masterpiece:
    def __init__(self, masterpiece_id: MasterpieceId):
        self._id = masterpiece_id

    @property
    def id(self) -> MasterpieceId:
        return self._id


class MasterpieceRepository:
    @abstractmethod
    def save(self, masterpiece: Masterpiece) -> None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def get(
            self, masterpiece_id: MasterpieceId,
    ) -> Masterpiece:  # pragma: no cover
        raise NotImplementedError
