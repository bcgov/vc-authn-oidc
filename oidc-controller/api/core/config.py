import json
import logging
import os
from enum import Enum
from functools import lru_cache
from typing import Optional

import requests
from pydantic import BaseSettings, PostgresDsn

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
    PSQL_HOST: str = os.environ.get("POSTGRESQL_HOST", "localhost")
    PSQL_PORT: int = os.environ.get("POSTGRESQL_PORT", "5432")
    PSQL_DB: str = os.environ.get("POSTGRESQL_DB", "traction")
    PSQL_USER: str = os.environ.get("OIDC_CONTROLLER_DB_USER", "oidccontrolleruser")
    PSQL_PASS: str = os.environ.get("OIDC_CONTROLLER_DB_USER_PWD", "oidccontrollerpass")

    PSQL_ADMIN_USER: str = os.environ.get(
        "OIDC_CONTROLLER_DB_ADMIN", "oidccontrolleradminuser"
    )
    PSQL_ADMIN_PASS: str = os.environ.get(
        "OIDC_CONTROLLER_DB_ADMIN_PWD", "oidccontrolleradminpass"
    )

    CONTROLLER_URL: str = os.environ.get("CONTROLLER_URL")
    # # Get CONTROLLER_URL from env or NGROK.
    CONTROLLER_NGROK: str = os.environ.get("CONTROLLER_NGROK")
    if not CONTROLLER_URL and CONTROLLER_NGROK:
        raw_resp = requests.get(CONTROLLER_NGROK + "/api/tunnels")
        resp = json.loads(raw_resp.content)
        CONTROLLER_URL = resp["tunnels"][0]["public_url"]
        print("loaded CONTROLLER_URL from NGROK_TUNNEL_HOST")
    print("CONTROLLER_URL: " + CONTROLLER_URL)

    #
    ACAPY_AGENT_URL: str = os.environ.get("ACAPY_AGENT_URL")
    ACAPY_NGROK_TUNNEL_HOST: str = os.environ.get("ACAPY_NGROK_TUNNEL_HOST")
    if not ACAPY_AGENT_URL and not ACAPY_NGROK_TUNNEL_HOST:
        print(
            "WARNING: neither ACAPY_AGENT_URL or ACAPY_NGROK_TUNNEL_HOST provided, agent will not be accessible"
        )

    if not ACAPY_AGENT_URL and ACAPY_NGROK_TUNNEL_HOST:
        raw_resp = requests.get(ACAPY_NGROK_TUNNEL_HOST + "/api/tunnels")
        resp = json.loads(raw_resp.content)
        https_tunnels = [t for t in resp["tunnels"] if t["proto"] == "https"]
        ACAPY_AGENT_URL = https_tunnels[0]["public_url"]
        print("loaded ACAPY_AGENT_URL from ACAPY_NGROK_TUNNEL_HOST")
    print("ACAPY_AGENT_URL: " + str(ACAPY_AGENT_URL))

    # application connection is async
    # fmt: off
    SQLALCHEMY_DATABASE_URI: PostgresDsn = (
        f"postgresql+asyncpg://{PSQL_USER}:{PSQL_PASS}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DB}"  # noqa: E501
    )

    # migrations connection uses owner role and is synchronous
    SQLALCHEMY_DATABASE_ADMIN_URI: PostgresDsn = (
        f"postgresql://{PSQL_ADMIN_USER}:{PSQL_ADMIN_PASS}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DB}"  # noqa: E501
    )

    ACAPY_TENANCY: str = os.environ.get("ACAPY_TENANCY", "single") # other option is "multi"

    ACAPY_ADMIN_URL: str = os.environ.get("ACAPY_ADMIN_URL", "http://localhost:8031")

    MT_ACAPY_WALLET_ID: str = os.environ.get("MT_ACAPY_WALLET_ID")
    MT_ACAPY_WALLET_KEY: str = os.environ.get("MT_ACAPY_WALLET_KEY", "random-key")

    ST_ACAPY_ADMIN_API_KEY_NAME: str = os.environ.get("ST_ACAPY_ADMIN_API_KEY_NAME")
    ST_ACAPY_ADMIN_API_KEY: str = os.environ.get("ST_ACAPY_ADMIN_API_KEY")
    DB_ECHO_LOG: bool = False

    DEFAULT_PAGE_SIZE: int = os.environ.get("DEFAULT_PAGE_SIZE", 10)

    # Allow CORS from a comma-separated list of origins
    TRACTION_CORS_URLS: str = os.environ.get("TRACTION_CORS_URLS", "")

    # openssl rand -hex 32
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 300

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
