import logging
from uuid import UUID
from pymongo import ReturnDocument

from fastapi import HTTPException
from fastapi import status as http_status
from fastapi.encoders import jsonable_encoder

from .models import (
    AuthSession,
    AuthSessionCreate,
    AuthSessionPatch,
)
from ..db.session import db, COLLECTION_NAMES


logger = logging.getLogger(__name__)


class AuthSessionCRUD:
    @classmethod
    async def create(cls, auth_session: AuthSessionCreate) -> AuthSession:
        col = db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
        result = col.insert_one(jsonable_encoder(auth_session))
        return AuthSession(**col.find_one({"_id": result.inserted_id}))

    @classmethod
    async def get(cls, auth_session_id: str) -> AuthSession:
        col = db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
        auth_sess = col.find_one({"_id": auth_session_id})

        if auth_sess is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The auth_session hasn't been found!",
            )

        return AuthSession(**auth_sess)

    @classmethod
    async def patch(cls, auth_session_id: str, data: AuthSessionPatch) -> AuthSession:
        col = db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
        auth_sess = col.find_one_and_update(
            {"_id": auth_session_id},
            {"$set": data.dict(exclude_unset=True)},
            return_document=ReturnDocument.AFTER,
        )

        return auth_sess

    @classmethod
    async def delete(cls, auth_session_id: str) -> bool:
        col = db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
        auth_sess = col.find_one_and_delete({"_id": auth_session_id})
        return bool(auth_sess)

    @classmethod
    async def get_by_pres_exch_id(cls, pres_exch_id: str) -> AuthSession:
        col = db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
        auth_sess = col.find_one({"pres_exch_id": pres_exch_id})

        if auth_sess is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The auth_session hasn't been found with that pres_exch_id!",
            )

        return AuthSession(**auth_sess)
