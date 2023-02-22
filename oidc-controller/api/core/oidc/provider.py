import logging

from urllib.parse import urlparse
from jwkest.jwk import rsa_load, RSAKey, KEYS

from pyop.authz_state import AuthorizationState
from pyop.provider import Provider
from pyop.storage import RedisWrapper
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

configuration_information = {
    "issuer": issuer_url,
    "authorization_endpoint": f"{issuer_url}/authorization",
    "token_endpoint": f"{issuer_url}/token",
    "jwks_uri": f"{issuer_url}/.well-known/openid-configuration/jwks",
    "response_types_supported": ["code", "id_token token"],
    "id_token_signing_alg_values_supported": [signing_key.alg],
    "response_modes_supported": ["fragment", "query"],
    "subject_types_supported": ["public", "pairwise"],
    "grant_types_supported": ["authorization_code", "implicit"],
    "claim_types_supported": ["normal"],
    "claims_parameter_supported": True,
    "claims_supported": ["sub", "name", "given_name", "family_name"],
    "request_parameter_supported": True,
    "request_uri_parameter_supported": False,
    "scopes_supported": ["openid", "profile"],
}

subject_id_factory = HashBasedSubjectIdentifierFactory("asdwadwa")
authz_state = AuthorizationState(
    subject_id_factory,
    RedisWrapper(db_uri, db_name="provider", collection="authz_codes"),
    RedisWrapper(db_uri, db_name="provider", collection="access_tokens"),
    RedisWrapper(db_uri, db_name="provider", collection="refresh_tokens"),
    RedisWrapper(db_uri, db_name="provider", collection="subject_identifiers"),
)
client_db = RedisWrapper(db_uri, db_name="provider", collection="clients")
user_db = RedisWrapper(db_uri, db_name="provider", collection="users")
provider = Provider(
    signing_key, configuration_information, authz_state, client_db, Userinfo(user_db)
)
