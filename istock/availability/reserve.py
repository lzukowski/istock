from .masterpiece import MasterpieceId, VariantId, OwnerId


class Reserve:
    def __call__(
            self,
            masterpiece_id: MasterpieceId,
            variant_id: VariantId,
            owner_id: OwnerId,
    ) -> bool:
        raise NotImplementedError
