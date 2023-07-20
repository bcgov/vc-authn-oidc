import structlog
import structlog.typing
import os

from api.core.config import settings
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pymongo.database import Database
from pyop.authz_state import AuthorizationState
from pyop.provider import Provider
from pyop.storage import StatelessWrapper
from pyop.subject_identifier import HashBasedSubjectIdentifierFactory
from pyop.userinfo import Userinfo
from urllib.parse import urlparse
from jwkest.jwk import rsa_load, RSAKey, KEYS

logger: structlog.typing.FilteringBoundLogger = structlog.get_logger()
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def get_signing_key_dir_path(to_replace_str, replacement_str, filename_str) -> str:
    """Get signing key directory."""
    file_path = DIR_PATH.replace(to_replace_str, replacement_str)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return os.path.join(file_path, filename_str)


def save_pem_file(filename, content):
    """Save the pem file in oidc-controller dir."""
    f = open(filename, "wb")
    f.write(content)
    f.close()


def pem_file_exists(filepath) -> bool:
    """Check if pem file exists."""
    return os.path.isfile(filepath)


if settings.TESTING:
    # Test pem file location /vc-authn-oidc/test-signing-keys.
    SIGNING_KEY_FILEPATH = get_signing_key_dir_path(
        to_replace_str="/oidc-controller/api/core/oidc",
        replacement_str="/test-signing-keys",
        filename_str="test_signing_key.pem",
    )
else:
    if not settings.SIGNING_KEY_FILEPATH:
        # Default pem file location /app/signing-keys.
        SIGNING_KEY_FILEPATH = get_signing_key_dir_path(
            to_replace_str="/api/core/oidc",
            replacement_str="/signing-keys",
            filename_str="signing_key.pem",
        )
    else:
        SIGNING_KEY_FILEPATH = settings.SIGNING_KEY_FILEPATH
        logger.info(
            f"SIGNING_KEY_FILEPATH {SIGNING_KEY_FILEPATH} env variable provided."
        )

if not pem_file_exists(SIGNING_KEY_FILEPATH):
    logger.info("creating new pem file")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=int(settings.SIGNING_KEY_SIZE),
        backend=default_backend(),
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    save_pem_file(SIGNING_KEY_FILEPATH, pem)
else:
    logger.info("pem file alrady exists")
logger.info(f"pem file located at {SIGNING_KEY_FILEPATH}.")

issuer_url = settings.CONTROLLER_URL
if urlparse(issuer_url).scheme != "https":
    logger.error("CONTROLLER_URL is not HTTPS. changing openid-config for development")
    issuer_url = issuer_url[:4] + "s" + issuer_url[4:]
signing_key = RSAKey(key=rsa_load(SIGNING_KEY_FILEPATH), use="sig", alg=settings.SIGNING_KEY_ALGORITHM)
signing_keys = KEYS().append(signing_key)

# config from vc-authn-oidc 1.0 can be found here
# https://toip-vc-authn-controller-dev.apps.silver.devops.gov.bc.ca/.well-known/openid-configuration

# TODO validate the correctness of this? either change config or add capabilities
configuration_information = {
    "issuer": issuer_url,
    "authorization_endpoint": f"{issuer_url}/authorization",
    "token_endpoint": f"{issuer_url}/token",
    "jwks_uri": f"{issuer_url}/.well-known/openid-configuration/jwks",
    "response_types_supported": ["code", "id_token", "token"],
    "id_token_signing_alg_values_supported": [signing_key.alg],
    "response_modes_supported": ["fragment", "query", "form_post"],
    "subject_types_supported": ["public"],
    "grant_types_supported": ["hybrid"],
    "claim_types_supported": ["normal"],
    "claims_parameter_supported": False,
    "request_parameter_supported": True,
    "request_uri_parameter_supported": False,
    "scopes_supported": ["openid"],
    "token_endpoint_auth_methods_supported": ["client_secret_basic"],
    "frontchannel_logout_supported": True,
    "frontchannel_logout_session_supported": True,
    "backchannel_logout_supported": True,
    "backchannel_logout_session_supported": True,
}

subject_id_factory = HashBasedSubjectIdentifierFactory(settings.SUBJECT_ID_HASH_SALT)

# placeholder that gets set on app_start and write operations to ClientConfigurationCRUD
provider = None


async def init_provider(db: Database):
    global provider
    from api.clientConfigurations.crud import ClientConfigurationCRUD

    all_client_configs = await ClientConfigurationCRUD(db).get_all()
    client_db = {d.client_name: d.dict() for d in all_client_configs}
    user_db = {"vc-user": {"sub": None}} # placeholder, this will be replaced by the subject defined in the proof-configuration

    provider = Provider(
        signing_key,
        configuration_information,
        AuthorizationState(subject_id_factory),
        client_db,
        Userinfo(user_db), 
    )
