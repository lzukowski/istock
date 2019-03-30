from .masterpiece import MasterpieceId


class Register:
    def __call__(
            self, masterpiece_id: MasterpieceId,
    ) -> None:  # pragma: no cover
        raise NotImplementedError
