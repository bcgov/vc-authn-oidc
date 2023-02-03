from fastapi import APIRouter, HTTPException
from fastapi import status as http_status
from ..core.models import StatusMessage

from .crud import VerificationConfigCRUD
from .models import (
    VerificationConfigPatch,
    VerificationConfigRead,
    VerificationConfig,
)

router = APIRouter()


@router.post(
    "/",
    response_description="Add new verification configuration",
    status_code=http_status.HTTP_201_CREATED,
    response_model=VerificationConfig,
    response_model_exclude_unset=True,
)
async def create_ver_config(ver_config: VerificationConfig):
    return await VerificationConfigCRUD.create(ver_config)


@router.get(
    "/{ver_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=VerificationConfigRead,
    response_model_exclude_unset=True,
)
async def get_ver_conf(
    ver_config_id: str,
):
    return await VerificationConfigCRUD.get(ver_config_id)


@router.patch(
    "/{ver_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=VerificationConfigRead,
    response_model_exclude_unset=True,
)
async def patch_ver_conf(
    ver_config_id: str,
    data: VerificationConfigPatch,
):
    return await VerificationConfigCRUD.patch(ver_config_id=ver_config_id, data=data)


@router.delete(
    "/{ver_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=StatusMessage,
)
async def delete_ver_conf_by_uuid(
    ver_config_id: str,
):
    status = await VerificationConfigCRUD.delete(ver_config_id=ver_config_id)

    if not status:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="ver_config does not exist",
        )
    return StatusMessage(status, "The ver_config was deleted")
