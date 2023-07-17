import logging
import os
from enum import Enum
from functools import lru_cache
from typing import Optional, Union

from pydantic import BaseSettings

logger = logging.getLogger(__name__)


class EnvironmentEnum(str, Enum):
    PRODUCTION = "production"
    LOCAL = "local"


class GlobalConfig(BaseSettings):
    TITLE: str = os.environ.get("CONTROLLER_APP_TITLE", "vc-authn-oidc Controller")
    DESCRIPTION: str = os.environ.get(
        "CONTROLLER_APP_DESCRIPTION",
        "An oidc authentication solution for verification credentials",
    )

    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False
    TESTING: bool = False
    TIMEZONE: str = "UTC"

    # the following defaults match up with default values in scripts/.env.example
    # these MUST be all set in non-local environments.
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_PORT: Union[int, str] = os.environ.get("DB_PORT", "27017")
    DB_NAME: str = os.environ.get("DB_NAME", "oidc-controller")
    DB_USER: str = os.environ.get("OIDC_CONTROLLER_DB_USER", "oidccontrolleruser")
    DB_PASS: str = os.environ.get("OIDC_CONTROLLER_DB_USER_PWD", "oidccontrollerpass")

    MONGODB_URL: str = f"""mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?retryWrites=true&w=majority"""  # noqa: E501

    CONTROLLER_URL: Optional[str] = os.environ.get("CONTROLLER_URL")
    # Where to send users when trying to scan with their mobile camera (not a wallet)
    CONTROLLER_CAMERA_REDIRECT_URL: Optional[str] = os.environ.get("CONTROLLER_CAMERA_REDIRECT_URL")
    # The number of seconds to wait for a presentation to be verified, Default: 10
    CONTROLLER_PRESENTATION_EXPIRE_TIME: Union[int, str] = os.environ.get("CONTROLLER_PRESENTATION_EXPIRE_TIME", 10)

    ACAPY_AGENT_URL: Optional[str] = os.environ.get("ACAPY_AGENT_URL")
    if not ACAPY_AGENT_URL:
        print("WARNING: ACAPY_AGENT_URL was not provided, agent will not be accessible")

    ACAPY_TENANCY: str = os.environ.get(
        "ACAPY_TENANCY", "single"
    )  # valid options are "multi" and "single"

    ACAPY_ADMIN_URL: str = os.environ.get("ACAPY_ADMIN_URL", "http://localhost:8031")

    MT_ACAPY_WALLET_ID: Optional[str] = os.environ.get("MT_ACAPY_WALLET_ID")
    MT_ACAPY_WALLET_KEY: str = os.environ.get("MT_ACAPY_WALLET_KEY", "random-key")

    ST_ACAPY_ADMIN_API_KEY_NAME: Optional[str] = os.environ.get("ST_ACAPY_ADMIN_API_KEY_NAME")
    ST_ACAPY_ADMIN_API_KEY: Optional[str] = os.environ.get("ST_ACAPY_ADMIN_API_KEY")
    DB_ECHO_LOG: bool = False

    DEFAULT_PAGE_SIZE: Union[int, str] = os.environ.get("DEFAULT_PAGE_SIZE", 10)

    # openssl rand -hex 32
    SIGNING_KEY_SIZE = os.environ.get("SIGNING_KEY_SIZE", 2048)
    # SIGNING_KEY_FILEPATH expects complete path including filename and extension.
    SIGNING_KEY_FILEPATH: Optional[str] = os.environ.get("SIGNING_KEY_FILEPATH")
    SIGNING_KEY_ALGORITHM: str = os.environ.get("SIGNING_KEY_ALGORITHM", "RS256")
    SUBJECT_ID_HASH_SALT = os.environ.get("SUBJECT_ID_HASH_SALT", "test_hash_salt")

    # OIDC Client Settings
    OIDC_CLIENT_ID: str = os.environ.get("OIDC_CLIENT_ID", "keycloak")
    OIDC_CLIENT_NAME: str = os.environ.get("OIDC_CLIENT_NAME", "keycloak")
    OIDC_CLIENT_REDIRECT_URI: str = os.environ.get(
        "OIDC_CLIENT_REDIRECT_URI",
        "http://localhost:8880/auth/realms/vc-authn/broker/vc-authn/endpoint",
    )
    OIDC_CLIENT_SECRET: str = os.environ.get("OIDC_CLIENT_SECRET", "**********")

    # OIDC Controller Settings
    CONTROLLER_API_KEY: str = os.environ.get("CONTROLLER_API_KEY", "")
    USE_OOB_PRESENT_PROOF: Union[bool, str] = os.environ.get("USE_OOB_PRESENT_PROOF", False)
    USE_OOB_LOCAL_DID_SERVICE: Union[bool, str] = os.environ.get("USE_OOB_LOCAL_DID_SERVICE", False)
    SET_NON_REVOKED: Union[bool, str] = os.environ.get("SET_NON_REVOKED", True)

    class Config:
        case_sensitive = True


class LocalConfig(GlobalConfig):
    """Local configurations."""

    DEBUG: bool = True
    DB_ECHO_LOG = True
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL


class ProdConfig(GlobalConfig):
    """Production configurations."""

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PRODUCTION


class FactoryConfig:
    def __init__(self, environment: Optional[str]):
        self.environment = environment

    def __call__(self) -> GlobalConfig:
        if self.environment == EnvironmentEnum.LOCAL.value:
            return LocalConfig()
        return ProdConfig()


@lru_cache()
def get_configuration() -> GlobalConfig:
    return FactoryConfig(os.environ.get("ENVIRONMENT"))()


settings = get_configuration()
