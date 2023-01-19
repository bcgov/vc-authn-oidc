import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..core.config import settings


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/.well-known/openid-configuration", response_class=JSONResponse)
async def get_well_known_oid_config():
    result = {
        "authorizationUrl": settings.CONTROLLER_NGROK + "/vc/connect/authorize",
        "tokenUrl": settings.CONTROLLER_NGROK + "/vc/connect/token",
    }
    return result
