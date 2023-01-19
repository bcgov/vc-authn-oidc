import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from oic.oauth2.message import ASConfigurationResponse
from ..core.config import settings


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/.well-known/openid-configuration", response_class=JSONResponse)
async def get_well_known_oid_config():
    result = ASConfigurationResponse(
        authorization_endpoint=settings.CONTROLLER_URL + "/vc/connect/authorize",
        token_endpoint=settings.CONTROLLER_URL + "/vc/connect/token",
    )
    return result
