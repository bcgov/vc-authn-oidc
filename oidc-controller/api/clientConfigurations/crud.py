import logging

from typing import List
from pymongo import ReturnDocument
from pymongo.database import Database
from fastapi import HTTPException
from fastapi import status as http_status
from fastapi.encoders import jsonable_encoder

from ..core.models import PyObjectId
from .models import (
    ClientConfiguration,
    ClientConfigurationCreate,
    ClientConfigurationPatch,
    ClientConfigurationRead,
)
from ..db.session import COLLECTION_NAMES


logger = logging.getLogger(__name__)


class ClientConfigurationCRUD:
    def __init__(self, db: Database):
        self._db = db

    async def create(
        self, client_config: ClientConfigurationCreate
    ) -> ClientConfiguration:
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFiGURATIONS)
        result = col.insert_one(jsonable_encoder(client_config))
        return ClientConfiguration(**col.find_one({"_id": result.inserted_id}))

    async def get(self, id: str) -> ClientConfigurationRead:
        if not PyObjectId.is_valid(id):
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}"
            )
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFiGURATIONS)
        obj = col.find_one({"_id": PyObjectId(id)})

        if obj is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The auth_session hasn't been found!",
            )

        return ClientConfiguration(**obj)

    async def get_all(self) -> List[ClientConfigurationRead]:
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFiGURATIONS)
        return [ClientConfigurationRead(**cc) for cc in col.find()]

    async def patch(
        self, id: str, data: ClientConfigurationPatch
    ) -> ClientConfiguration:
        if not PyObjectId.is_valid(id):
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}"
            )
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFiGURATIONS)
        obj = col.find_one_and_update(
            {"_id": PyObjectId(id)},
            {"$set": data.dict(exclude_unset=True)},
            return_document=ReturnDocument.AFTER,
        )

        return obj

    async def delete(self, id: str) -> bool:
        if not PyObjectId.is_valid(id):
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}"
            )
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFiGURATIONS)
        obj = col.find_one_and_delete({"_id": PyObjectId(id)})
        return bool(obj)
