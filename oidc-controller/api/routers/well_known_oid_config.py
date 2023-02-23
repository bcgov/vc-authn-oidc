import logging, json

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

# from oic.oauth2.message import ASConfigurationResponse
from jwkest.jwk import RSAKey, KEYS
from ..core.oidc import provider

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/.well-known/openid-configuration", response_class=JSONResponse)
async def get_well_known_oid_config():
    """returns configuration response compliant with https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfigurationResponse"""
    return provider.configuration_information


@router.get("/.well-known/openid-configuration/jwks", response_class=JSONResponse)
async def get_well_known_jwks():
    return {"keys": [provider.signing_key.to_dict()]}
