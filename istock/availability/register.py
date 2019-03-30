from injector import inject

from .masterpiece import MasterpieceId, Masterpiece, MasterpieceRepository


class Register:
    @inject
    def __init__(self, masterpiece_repo: MasterpieceRepository) -> None:
        self._repo = masterpiece_repo

    def __call__(self, masterpiece_id: MasterpieceId) -> None:
        masterpiece = Masterpiece(masterpiece_id)
        self._repo.save(masterpiece)
