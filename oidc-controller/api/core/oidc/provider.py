from jwkest.jwk import rsa_load, RSAKey

from pyop.authz_state import AuthorizationState
from pyop.provider import Provider
from pyop.storage import RedisWrapper
from pyop.subject_identifier import HashBasedSubjectIdentifierFactory
from pyop.userinfo import Userinfo

from ..config import settings

db_uri = settings.REDISDB_URL


signing_key = RSAKey(key=rsa_load("signing_key.pem"), use="sig", alg="RS256")

configuration_information = {
    "issuer": "https://controller:5201",
    "authorization_endpoint": "https://controller:5201/authorization",
    "token_endpoint": "https://controller:5201/token",
    "userinfo_endpoint": "https://controller:5201/userinfo",
    "registration_endpoint": "https://controller:5201/registration",
    "jwks_uri": "https://controller:5201/.well-known/openid-configuration/jwks",
    "response_types_supported": ["code", "id_token token"],
    "id_token_signing_alg_values_supported": [signing_key.alg],
    "response_modes_supported": ["fragment", "query"],
    "subject_types_supported": ["public", "pairwise"],
    "grant_types_supported": ["authorization_code", "implicit"],
    "claim_types_supported": ["normal"],
    "claims_parameter_supported": True,
    "claims_supported": ["sub", "name", "given_name", "family_name"],
    "request_parameter_supported": False,
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
