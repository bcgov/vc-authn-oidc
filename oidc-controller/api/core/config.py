import json
import logging
import sys
import logging.config
import structlog
import os
from enum import Enum
from functools import lru_cache
from typing import Optional, Union

from pydantic import BaseSettings

from pathlib import Path


# Use environment variable to determine logging format
# fallback to logconf.json
# finally default to true
# bool() is needed to coerce the results of the environment variable
use_json_logs: bool = bool(os.environ.get("LOG_WITH_JSON", True))

time_stamp_format: str = os.environ.get("LOG_TIMESTAMP_FORMAT", "iso")

with open((Path(__file__).parent.parent / "logconf.json").resolve()) as user_file:
    file_contents: dict = json.loads(user_file.read())
    logging.config.dictConfig(file_contents["logger"])


def determin_log_level():
    match os.environ.get("LOG_LEVEL"):
        case "DEBUG":
            return logging.DEBUG
        case "INFO":
            return logging.INFO
        case "WARNING":
            return logging.WARNING
        case "ERROR":
            return logging.ERROR
        case _:
            return logging.NOTSET


logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=determin_log_level(),
)

shared_processors = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.stdlib.ExtraAdder(),
    structlog.processors.StackInfoRenderer(),
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt=time_stamp_format),
]

renderer = (
    structlog.processors.JSONRenderer()
    if use_json_logs
    else structlog.dev.ConsoleRenderer()
)

# override uvicorn logging to use logstruct
formatter = structlog.stdlib.ProcessorFormatter(
    # These run ONLY on `logging` entries that do NOT originate within
    # structlog.
    foreign_pre_chain=shared_processors,
    # These run on ALL entries after the pre_chain is done.
    processors=[
        # Remove _record & _from_structlog.
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        renderer,
    ],
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

for _log in ["uvicorn", "uvicorn.error"]:
    # Clear the log handlers for uvicorn loggers, and enable propagation
    # so the messages are caught by our root logger and formatted correctly
    # by structlog
    logging.getLogger(_log).handlers.clear()
    logging.getLogger(_log).addHandler(handler)
    logging.getLogger(_log).propagate = False

# This is already handled by our middleware
logging.getLogger("uvicorn.access").handlers.clear()
logging.getLogger("uvicorn.access").propagate = False

# Configure structlog
structlog.configure(
    processors=[structlog.stdlib.filter_by_level] + shared_processors + [renderer],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(
        logging.getLogger().getEffectiveLevel()
    ),
    cache_logger_on_first_use=True,
)

# Setup logger for config
logger: structlog.typing.FilteringBoundLogger = structlog.getLogger(__name__)


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
    CONTROLLER_CAMERA_REDIRECT_URL: Optional[str] = os.environ.get(
        "CONTROLLER_CAMERA_REDIRECT_URL"
    )
    # The number of seconds to wait for a presentation to be verified, Default: 10
    CONTROLLER_PRESENTATION_EXPIRE_TIME: Union[int, str] = os.environ.get(
        "CONTROLLER_PRESENTATION_EXPIRE_TIME", 10
    )

    ACAPY_AGENT_URL: Optional[str] = os.environ.get("ACAPY_AGENT_URL")
    if not ACAPY_AGENT_URL:
        logger.warning("ACAPY_AGENT_URL was not provided, agent will not be accessible")

    ACAPY_TENANCY: str = os.environ.get(
        "ACAPY_TENANCY", "single"
    )  # valid options are "multi" and "single"

    ACAPY_ADMIN_URL: str = os.environ.get("ACAPY_ADMIN_URL", "http://localhost:8031")

    MT_ACAPY_WALLET_ID: Optional[str] = os.environ.get("MT_ACAPY_WALLET_ID")
    MT_ACAPY_WALLET_KEY: str = os.environ.get("MT_ACAPY_WALLET_KEY", "random-key")

    ST_ACAPY_ADMIN_API_KEY_NAME: Optional[str] = os.environ.get(
        "ST_ACAPY_ADMIN_API_KEY_NAME"
    )
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
    USE_OOB_PRESENT_PROOF: bool = bool(os.environ.get("USE_OOB_PRESENT_PROOF", False))
    USE_OOB_LOCAL_DID_SERVICE: bool = bool(
        os.environ.get("USE_OOB_LOCAL_DID_SERVICE", False)
    )
    SET_NON_REVOKED: bool = bool(os.environ.get("SET_NON_REVOKED", True))

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
