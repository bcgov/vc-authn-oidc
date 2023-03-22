import logging

from pymongo import ReturnDocument
from pymongo.database import Database
from fastapi import HTTPException
from fastapi import status as http_status
from fastapi.encoders import jsonable_encoder

from ..core.models import PyObjectId
from .models import (
    AuthSession,
    AuthSessionCreate,
    AuthSessionPatch,
)
from api.db.session import COLLECTION_NAMES
from api.core.oidc.provider import init_provider


logger = logging.getLogger(__name__)


class AuthSessionCRUD:
    def __init__(self, db: Database):
        self._db = db

    async def create(self, auth_session: AuthSessionCreate) -> AuthSession:
        col = self._db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
        result = col.insert_one(jsonable_encoder(auth_session))
        return AuthSession(**col.find_one({"_id": result.inserted_id}))

    async def get(self, auth_session_id: str) -> AuthSession:
        if not PyObjectId.is_valid(auth_session_id):
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}"
            )
        col = self._db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
        auth_sess = col.find_one({"_id": PyObjectId(auth_session_id)})

        if auth_sess is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The auth_session hasn't been found!",
            )

        return AuthSession(**auth_sess)

    async def patch(self, auth_session_id: str, data: AuthSessionPatch) -> AuthSession:
        col = self._db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
        auth_sess = col.find_one_and_update(
            {"_id": auth_session_id},
            {"$set": data.dict(exclude_unset=True)},
            return_document=ReturnDocument.AFTER,
        )

        return auth_sess

    async def delete(self, auth_session_id: str) -> bool:
        if not PyObjectId.is_valid(id):
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}"
            )
        col = self._db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
        auth_sess = col.find_one_and_delete({"_id": PyObjectId(auth_session_id)})
        return bool(auth_sess)

    async def get_by_pres_exch_id(self, pres_exch_id: str) -> AuthSession:
        col = self._db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
        auth_sess = col.find_one({"pres_exch_id": pres_exch_id})

        if auth_sess is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The auth_session hasn't been found with that pres_exch_id!",
            )

        return AuthSession(**auth_sess)

    async def get_by_pyop_auth_code(self, code: str) -> AuthSession:
        col = self._db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
        auth_sess = col.find_one({"pyop_auth_code": code})

        if auth_sess is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The auth_session hasn't been found with that pyop_auth_code!",
            )

        return AuthSession(**auth_sess)
