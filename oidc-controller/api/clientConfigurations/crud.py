import logging

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

    async def get(self, id: str) -> ClientConfiguration:
        if not PyObjectId.is_valid(id):
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}"
            )
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFiGURATIONS)
        auth_sess = col.find_one({"_id": PyObjectId(id)})

        if auth_sess is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The auth_session hasn't been found!",
            )

        return ClientConfiguration(**auth_sess)

    async def patch(
        self, id: str, data: ClientConfigurationPatch
    ) -> ClientConfiguration:
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFiGURATIONS)
        auth_sess = col.find_one_and_update(
            {"_id": id},
            {"$set": data.dict(exclude_unset=True)},
            return_document=ReturnDocument.AFTER,
        )

        return auth_sess

    async def delete(self, auth_session_id: str) -> bool:
        col = self._db.get_collection(COLLECTION_NAMES.CLIENT_CONFiGURATIONS)
        auth_sess = col.find_one_and_delete({"_id": auth_session_id})
        return bool(auth_sess)
