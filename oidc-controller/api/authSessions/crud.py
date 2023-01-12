import logging
from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import (
    AuthSession,
    AuthSessionCreate,
    AuthSessionPatch,
)

logger = logging.getLogger(__name__)


class AuthSessionCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: AuthSessionCreate) -> AuthSession:
        values = data.dict()

        auth_session = AuthSession(**values)
        self.session.add(auth_session)
        await self.session.commit()
        await self.session.refresh(auth_session)

        return auth_session

    async def get(self, auth_session_id: str) -> AuthSession:
        statement = select(AuthSession).where(AuthSession.uuid == auth_session_id)
        results = await self.session.execute(statement=statement)
        ver_conf = results.scalar_one_or_none()  # type: AuthSession | None

        if ver_conf is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The auth_session hasn't been found!",
            )

        return ver_conf

    async def patch(self, auth_session_id: str, data: AuthSessionPatch) -> AuthSession:
        auth_session = await self.get(auth_session_id=auth_session_id)
        values = data.dict(exclude_unset=True)

        for k, v in values.items():
            setattr(auth_session, k, v)

        self.session.add(auth_session)
        await self.session.commit()
        await self.session.refresh(auth_session)

        return auth_session

    async def delete(self, auth_session_id: str) -> bool:
        statement = delete(AuthSession).where(AuthSession.uuid == auth_session_id)

        await self.session.execute(statement=statement)
        await self.session.commit()

        return True

    async def get_by_pres_exch_id(self, pres_exch_id: str) -> AuthSession:
        statement = select(AuthSession).where(AuthSession.pres_exch_id == pres_exch_id)
        results = await self.session.execute(statement=statement)
        auth_session = results.scalar_one_or_none()  # type: AuthSession | None
        if auth_session is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The auth_session hasn't been found!",
            )

        return auth_session
