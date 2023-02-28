import logging
import redis
import json

from urllib.parse import urlparse
from jwkest.jwk import rsa_load, RSAKey, KEYS

from pyop.authz_state import AuthorizationState
from pyop.provider import Provider
from pyop.storage import RedisWrapper, StatelessWrapper
from pyop.subject_identifier import HashBasedSubjectIdentifierFactory
from pyop.userinfo import Userinfo


from ..config import settings

logger = logging.getLogger(__name__)

db_uri = settings.REDISDB_URL
issuer_url = settings.CONTROLLER_URL

if urlparse(issuer_url).scheme != "https":
    logger.warning(
        "WARNING CONTROLLER_URL is not HTTPS... MALFORMING openid-configuration for local development"
    )
    issuer_url = issuer_url[3:] + "s" + issuer_url[:3]

signing_key = RSAKey(key=rsa_load("signing_key.pem"), use="sig", alg="RS256")
signing_keys = KEYS().append(signing_key)

# config from vc-authn-oidc 1.0
# configuration_information = {
#     "issuer": issuer_url,
#     "authorization_endpoint": f"{issuer_url}/authorization",
#     "token_endpoint": f"{issuer_url}/token",
#     "jwks_uri": f"{issuer_url}/.well-known/openid-configuration/jwks",
#     "id_token_signing_alg_values_supported": [signing_key.alg],
#     "response_modes_supported": ["form_post", "query", "fragment"],
#     "claims_supported": [],
#     "scopes_supported": ["openid", "profile", "offline_access"],
#     "grant_types_supported": [
#         "authorization_code",
#         "client_credentials",
#         "refresh_token",
#         "implicit",
#         "urn:ietf:params:oauth:grant-type:device_code",
#     ],
#     "response_types_supported": [
#         "code",
#         "token",
#         "id_token",
#         "id_token token",
#         "code id_token",
#         "code token",
#         "code id_token token",
#     ],
#     "token_endpoint_auth_methods_supported": [
#         "client_secret_basic",
#         "client_secret_post",
#         "client_secret_query",
#     ],
#     "code_challenge_methods_supported": ["plain", "S256"],
#     "request_parameter_supported": True,
#     "frontchannel_logout_supported": True,
#     "frontchannel_logout_session_supported": True,
#     "backchannel_logout_supported": True,
#     "backchannel_logout_session_supported": True,
# }

# # TO BE REVIEWED
configuration_information = {
    "issuer": issuer_url,
    "authorization_endpoint": f"{issuer_url}/authorization",
    "token_endpoint": f"{issuer_url}/token",
    "jwks_uri": f"{issuer_url}/.well-known/openid-configuration/jwks",
    "response_types_supported": ["code", "id_token", "token"],
    "id_token_signing_alg_values_supported": [signing_key.alg],
    "response_modes_supported": ["fragment", "query"],
    "subject_types_supported": ["public", "pairwise"],
    "grant_types_supported": ["hybrid"],
    "claim_types_supported": ["normal"],
    "claims_parameter_supported": True,
    "claims_supported": ["sub"],
    "request_parameter_supported": True,
    "request_uri_parameter_supported": False,
    "scopes_supported": ["openid", "profile"],
    "token_endpoint_auth_methods_supported": ["client_secret_basic"],
}

subject_id_factory = HashBasedSubjectIdentifierFactory("asdwadwa")


kc_client = {
    "enabled": True,
    "client_id": "keycloak",
    "client_name": "keycloak",
    "allowed_grant_types": ["implicit", "code"],
    "allowed_scopes": ["openid", "profile", "vc_authn"],
    "response_types": ["code", "id_token", "token"],
    "redirect_uris": [
        "http://localhost:8880/auth/realms/vc-authn/broker/vc-authn/endpoint"
    ],
    "token_endpoint_auth_method": "client_secret_basic",
    "require_client_secret": True,
    "client_secret": "12345678",
    "require_consent": False,
}


provider = Provider(
    signing_key,
    configuration_information,
    AuthorizationState(subject_id_factory),
    {"keycloak": kc_client},
    Userinfo({"Jason": {"sub": "Jason"}}),
)
print(provider.clients)
