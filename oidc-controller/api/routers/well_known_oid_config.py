import logging, json

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


# from oic.oauth2.message import ASConfigurationResponse
from jwkest.jwk import RSAKey, KEYS


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/.well-known/openid-configuration", response_class=JSONResponse)
async def get_well_known_oid_config(request: Request):
    """returns configuration response compliant with https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfigurationResponse"""
    endpoint = request.app.server.server_get("endpoint", "provider_config")
    args = endpoint.process_request()
    response = endpoint.do_response(**args)
    resp = json.loads(response["response"])
    return resp


@router.get("/.well-known/openid-configuration/jwks", response_class=JSONResponse)
async def get_well_known_oid_config():
    """returns configuration response compliant with https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfigurationResponse"""
    key = RSAKey().load("signing_key.pem")
    jwks = KEYS()
    jwks.append(key)
    return json.loads(jwks.dump_jwks())
