from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_async_session
from .crud import VerificationConfigCRUD


async def get_verification_configs_crud(
    session: AsyncSession = Depends(get_async_session),
) -> VerificationConfigCRUD:
    return VerificationConfigCRUD(session=session)
