from fastapi import HTTPException
from fastapi import status as http_status
from fastapi.encoders import jsonable_encoder

from pymongo import ReturnDocument

from ..db.session import db, COLLECTION_NAMES

from .models import (
    VerificationConfig,
    VerificationConfigPatch,
)


class VerificationConfigCRUD:
    @classmethod
    async def create(cls, ver_config: VerificationConfig) -> VerificationConfig:
        ver_confs = db.get_collection(COLLECTION_NAMES.VER_CONFIGS)
        ver_confs.insert_one(jsonable_encoder(ver_config))
        return ver_confs.find_one({"ver_config_id": ver_config.ver_config_id})

    @classmethod
    async def get(cls, ver_config_id: str) -> VerificationConfig:
        ver_confs = db.get_collection(COLLECTION_NAMES.VER_CONFIGS)
        ver_conf = ver_confs.find_one({"ver_config_id": ver_config_id})

        if ver_conf is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The verification_config hasn't been found!",
            )

        return VerificationConfig(**ver_conf)

    @classmethod
    async def patch(
        cls, ver_config_id: str, data: VerificationConfigPatch
    ) -> VerificationConfig:
        ver_confs = db.get_collection(COLLECTION_NAMES.VER_CONFIGS)
        ver_conf = ver_confs.find_one_and_update(
            {"ver_config_id": ver_config_id},
            {"$set": data.dict(exclude_unset=True)},
            return_document=ReturnDocument.AFTER,
        )

        return ver_conf

    @classmethod
    async def delete(cls, ver_config_id: str) -> bool:
        ver_confs = db.get_collection(COLLECTION_NAMES.VER_CONFIGS)
        ver_conf = ver_confs.find_one_and_delete({"ver_config_id": ver_config_id})
        return bool(ver_conf)
