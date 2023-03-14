from pymongo.database import Database

from fastapi import APIRouter, HTTPException, Depends
from fastapi import status as http_status

from ..core.models import StatusMessage

from .crud import VerificationConfigCRUD
from .models import (
    VerificationConfigPatch,
    VerificationConfigRead,
    VerificationConfig,
)
from ..core.auth import get_api_key
from ..db.session import get_db

router = APIRouter()


@router.post(
    "/",
    response_description="Add new verification configuration",
    status_code=http_status.HTTP_201_CREATED,
    response_model=VerificationConfig,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_api_key)],
)
async def create_ver_config(
    ver_config: VerificationConfig, db: Database = Depends(get_db)
):
    return await VerificationConfigCRUD(db).create(ver_config)


@router.get(
    "/{ver_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=VerificationConfigRead,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_api_key)],
)
async def get_ver_conf(ver_config_id: str, db: Database = Depends(get_db)):
    return await VerificationConfigCRUD(db).get(ver_config_id)


@router.patch(
    "/{ver_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=VerificationConfigRead,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_api_key)],
)
async def patch_ver_conf(
    ver_config_id: str, data: VerificationConfigPatch, db: Database = Depends(get_db)
):
    return await VerificationConfigCRUD(db).patch(
        ver_config_id=ver_config_id, data=data
    )


@router.delete(
    "/{ver_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=StatusMessage,
    dependencies=[Depends(get_api_key)],
)
async def delete_ver_conf_by_uuid(ver_config_id: str, db: Database = Depends(get_db)):
    status = await VerificationConfigCRUD(db).delete(ver_config_id=ver_config_id)

    if not status:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="ver_config does not exist",
        )
    return StatusMessage(status=status, message="The ver_config was deleted")
