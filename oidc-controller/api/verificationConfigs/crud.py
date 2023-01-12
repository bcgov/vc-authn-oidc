from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError


from .models import (
    VerificationConfig,
    VerificationConfigCreate,
    VerificationConfigPatch,
)


class VerificationConfigCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: VerificationConfigCreate) -> VerificationConfig:
        values = data.dict()

        ver_config = VerificationConfig(**values)
        self.session.add(ver_config)
        try:
            await self.session.commit()
        except IntegrityError as e:
            raise HTTPException(status_code=422, detail=str(e))

        await self.session.refresh(ver_config)

        return ver_config

    async def get(self, ver_config_id: str) -> VerificationConfig:
        statement = select(VerificationConfig).where(
            VerificationConfig.ver_config_id == ver_config_id
        )
        results = await self.session.execute(statement=statement)
        ver_conf = results.scalar_one_or_none()  # type: VerificationConfig | None

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
