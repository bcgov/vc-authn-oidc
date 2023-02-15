import logging, json

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from oic.oauth2.message import ASConfigurationResponse
from jwkest.jwk import RSAKey, KEYS

from ..core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/.well-known/openid-configuration", response_class=JSONResponse)
async def get_well_known_oid_config():
    """returns configuration response compliant with https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfigurationResponse"""
    result = ASConfigurationResponse(
        issuer=settings.CONTROLLER_URL,
        authorization_endpoint=settings.CONTROLLER_URL + "/vc/connect/authorize",
        token_endpoint=settings.CONTROLLER_URL + "/vc/connect/token",
        jwks_uri=settings.CONTROLLER_URL + "/.well-known/openid-configuration/jwks",
    )

    return result


@router.get("/.well-known/openid-configuration/jwks", response_class=JSONResponse)
async def get_well_known_oid_config():
    """returns configuration response compliant with https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfigurationResponse"""
    key = RSAKey().load("signing_key.pem")
    jwks = KEYS()
    jwks.append(key)
    return json.loads(jwks.dump_jwks())
