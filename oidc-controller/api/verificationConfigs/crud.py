from fastapi import HTTPException
from fastapi import status as http_status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from ..core.config import settings

from ..db.session import db
from ..db import COLLECTIONS

from .models import (
    VerificationConfig,
    VerificationConfigCreate,
    VerificationConfigPatch,
)


class VerificationConfigCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    async def create(cls, ver_config: VerificationConfig) -> VerificationConfig:
        ver_confs = db.get_collection(COLLECTIONS.VER_CONFIGS)
        ver_confs.insert_one(jsonable_encoder(ver_config))
        return ver_confs.find_one({"ver_config_id": ver_config.ver_config_id})

    @classmethod
    async def get(self, ver_config_id: str) -> VerificationConfig:
        ver_confs = db.get_collection(COLLECTIONS.VER_CONFIGS)
        ver_conf = ver_confs.find_one({"ver_config_id": ver_config_id})

        if ver_conf is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The verification_config hasn't been found!",
            )

        return ver_conf

    async def patch(
        self, ver_config_id: str, data: VerificationConfigPatch
    ) -> VerificationConfig:
        ver_config = await self.get(ver_config_id=ver_config_id)
        values = data.dict(exclude_unset=True)

        for k, v in values.items():
            setattr(ver_config, k, v)

        self.session.add(ver_config)
        await self.session.commit()
        await self.session.refresh(ver_config)

        return ver_config

    async def delete(self, ver_config_id: str) -> bool:
        statement = delete(VerificationConfig).where(
            VerificationConfig.ver_config_id == ver_config_id
        )

        await self.session.execute(statement=statement)
        await self.session.commit()

        return True
