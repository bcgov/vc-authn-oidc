from typing import Union, Callable

from fastapi import HTTPException
from fastapi import status as http_status
from fastapi.encoders import jsonable_encoder

from pymongo import ReturnDocument, MongoClient
from pymongo.database import Database

from ..db.session import get_db, COLLECTION_NAMES

from .models import (
    VerificationConfig,
    VerificationConfigPatch,
)


class VerificationConfigCRUD:
    _db: Database = None

    def __init__(self, db: Database):
        self._db = db

    async def create(self, ver_config: VerificationConfig) -> VerificationConfig:
        print(self._db)
        ver_confs = self._db.get_collection(COLLECTION_NAMES.VER_CONFIGS)
        ver_confs.insert_one(jsonable_encoder(ver_config))
        return ver_confs.find_one({"ver_config_id": ver_config.ver_config_id})

    async def get(self, ver_config_id: str) -> VerificationConfig:
        ver_confs = self._db.get_collection(COLLECTION_NAMES.VER_CONFIGS)
        ver_conf = ver_confs.find_one({"ver_config_id": ver_config_id})

        if ver_conf is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The verification_config hasn't been found!",
            )

        return VerificationConfig(**ver_conf)

    async def patch(
        self, ver_config_id: str, data: VerificationConfigPatch
    ) -> VerificationConfig:
        ver_confs = self._db.get_collection(COLLECTION_NAMES.VER_CONFIGS)
        ver_conf = ver_confs.find_one_and_update(
            {"ver_config_id": ver_config_id},
            {"$set": data.dict(exclude_unset=True)},
            return_document=ReturnDocument.AFTER,
        )

        return ver_conf

    async def delete(self, ver_config_id: str) -> bool:
        ver_confs = self._db.get_collection(COLLECTION_NAMES.VER_CONFIGS)
        ver_conf = ver_confs.find_one_and_delete({"ver_config_id": ver_config_id})
        return bool(ver_conf)
