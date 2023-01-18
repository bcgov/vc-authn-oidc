from fastapi import APIRouter, Depends
from fastapi import status as http_status

from ..core.models import StatusMessage

from .crud import VerificationConfigCRUD
from .dependencies import get_verification_configs_crud
from .models import (
    VerificationConfigCreate,
    VerificationConfigPatch,
    VerificationConfigRead,
)

router = APIRouter()


@router.post(
    "", response_model=VerificationConfigRead, status_code=http_status.HTTP_201_CREATED
)
async def create_ver_conf(
    data: VerificationConfigCreate,
    ver_conf: VerificationConfigCRUD = Depends(get_verification_configs_crud),
):
    ver_conf = await ver_conf.create(data=data)

    return ver_conf


@router.get(
    "/{ver_config_id}",
    response_model=VerificationConfigRead,
    status_code=http_status.HTTP_200_OK,
)
async def get_ver_conf_by_uuid(
    ver_config_id: str,
    ver_configs: VerificationConfigCRUD = Depends(get_verification_configs_crud),
):
    ver_config = await ver_configs.get(ver_config_id=ver_config_id)

    return ver_config


@router.patch(
    "/{ver_config_id}",
    response_model=VerificationConfigRead,
    status_code=http_status.HTTP_200_OK,
)
async def patch_ver_conf_by_uuid(
    ver_config_id: str,
    data: VerificationConfigPatch,
    ver_configs: VerificationConfigCRUD = Depends(get_verification_configs_crud),
):
    ver_conf = await ver_configs.patch(ver_config_id=ver_config_id, data=data)

    return ver_conf


@router.delete(
    "/{ver_config_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_ver_conf_by_uuid(
    ver_config_id: str,
    ver_confes: VerificationConfigCRUD = Depends(get_verification_configs_crud),
):
    status = await ver_confes.delete(ver_config_id=ver_config_id)

    return {"status": status, "message": "The ver_conf has been deleted!"}
