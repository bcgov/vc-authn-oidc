from pymongo.database import Database

from fastapi import APIRouter, HTTPException, Depends
from fastapi import status as http_status

from ..core.models import StatusMessage

from .crud import ClientConfigurationCRUD
from .models import (
    ClientConfigurationRead,
    ClientConfigurationPatch,
    ClientConfigurationCreate,
)
from ..core.auth import get_api_key
from ..db.session import get_db

router = APIRouter()


@router.post(
    "/",
    response_description="Add new verification configuration",
    status_code=http_status.HTTP_201_CREATED,
    response_model=ClientConfigurationCreate,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_api_key)],
)
async def create_client_config(
    ver_config: ClientConfigurationCreate, db: Database = Depends(get_db)
):
    return await ClientConfigurationCRUD(db).create(ver_config)


@router.get(
    "/",
    status_code=http_status.HTTP_200_OK,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_api_key)],
)
async def get_all_client_configs(db: Database = Depends(get_db)):
    return await ClientConfigurationCRUD(db).get_all()


@router.get(
    "/{client_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=ClientConfigurationRead,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_api_key)],
)
async def get_client_config(client_config_id: str, db: Database = Depends(get_db)):
    return await ClientConfigurationCRUD(db).get(client_config_id)


@router.patch(
    "/{client_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=ClientConfigurationRead,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_api_key)],
)
async def patch_client_config(
    client_config_id: str,
    data: ClientConfigurationPatch,
    db: Database = Depends(get_db),
):
    return await ClientConfigurationCRUD(db).patch(id=client_config_id, data=data)


@router.delete(
    "/{client_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=StatusMessage,
    dependencies=[Depends(get_api_key)],
)
async def delete_client_config(client_config_id: str, db: Database = Depends(get_db)):
    status = await ClientConfigurationCRUD(db).delete(id=client_config_id)

    if not status:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="client_config does not exist",
        )
    return StatusMessage(status=status, message="The client_config was deleted")
