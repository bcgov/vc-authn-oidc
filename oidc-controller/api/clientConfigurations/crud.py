import logging

from typing import List
from pymongo import ReturnDocument
from pymongo.database import Database
from fastapi import HTTPException
from fastapi import status as http_status
from fastapi.encoders import jsonable_encoder

from .models import (
    ClientConfiguration,
    ClientConfigurationCreate,
    ClientConfigurationPatch,
    ClientConfigurationRead,
)
from ..db.session import COLLECTION_NAMES
from api.core.oidc.provider import init_provider


logger = logging.getLogger(__name__)


class ClientConfigurationCRUD:
    def __init__(self, db: Database):
        self._db = db

    async def create(
        self, client_config: ClientConfigurationCreate
    ) -> ClientConfiguration:
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFIGURATIONS)
        col.insert_one(jsonable_encoder(client_config))

        # remake provider instance to refresh provider client
        await init_provider(self._db)
        return ClientConfiguration(
            **col.find_one({"client_id": client_config.client_id})
        )

    async def get(self, client_id: str) -> ClientConfigurationRead:
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFIGURATIONS)
        obj = col.find_one({"client_id": client_id})

        if obj is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The client_config hasn't been found!",
            )

        return ClientConfiguration(**obj)

    async def get_all(self) -> List[ClientConfigurationRead]:
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFIGURATIONS)
        return [ClientConfigurationRead(**cc) for cc in col.find()]

    async def patch(
        self, client_id: str, data: ClientConfigurationPatch
    ) -> ClientConfiguration:
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFIGURATIONS)
        obj = col.find_one_and_update(
            {"client_id": client_id},
            {"$set": data.dict(exclude_unset=True)},
            return_document=ReturnDocument.AFTER,
        )
        # remake provider instance to refresh provider client
        await init_provider(self._db)
        return obj

    async def delete(self, client_id: str) -> bool:
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFIGURATIONS)
        obj = col.find_one_and_delete({"client_id": client_id})

        # remake provider instance to refresh provider client
        await init_provider(self._db)

        return bool(obj)
