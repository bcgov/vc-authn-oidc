import json
import structlog
from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection
from pymongo.errors import OperationFailure
from pathlib import Path
from api.core.config import settings
from .collections import COLLECTION_NAMES
from ..authSessions.models import AuthSessionState


async def get_async_session():
    yield None


client = MongoClient(settings.MONGODB_URL, uuidRepresentation="standard")
logger: structlog.typing.FilteringBoundLogger = structlog.getLogger(__name__)


def index_name(k: str) -> str:
    return k + "_ttl"


def create_ttl_indexes(auth_session: Collection, file: str):
    auth_session_states: list[str] = [str(i) for i in list(AuthSessionState)]
    # Drop all old indexes if they exist
    for state in auth_session_states:
        try:
            auth_session.drop_index(index_name(state))
        except OperationFailure as _:
            # If this index does not exist just continue
            pass
    try:
        with open(Path(file).resolve()) as user_file:
            expiration_times: dict[str, int] = json.loads(user_file.read())
            # Ensure the given config is valid
            if not all(
                isinstance(k, str) and (k in auth_session_states) and isinstance(v, int)
                for k, v in expiration_times.items()
            ):
                raise Exception("Invalid json formatting")

    except Exception as e:
        match e:
            case FileNotFoundError():
                logger.warning(
                    "The file "
                    + file
                    + " does not exist or could not be opened "
                    + "because of this no auth session timeouts will be applied.",
                )
            case json.JSONDecodeError():
                logger.warning(
                    "Failed to decode the auth session timeouts timout config file "
                    + file
                    + " with the following error "
                    + str(e),
                )
            case Exception():
                logger.error(
                    "There is at least one invalid entry in the file "
                    + file
                    + ". Ensure all entries in your session timout file map an "
                    + "AuthSessionState to an integer "
                    + "valid auth session strings are "
                    + str(auth_session_states)
                    + " No expiration times will be applied",
                )
    else:
        # Create all indexes based on the config file
        for k, v in expiration_times.items():
            auth_session.create_index(
                [("created_at", ASCENDING)],
                expireAfterSeconds=v + settings.CONTROLLER_PRESENTATION_BUFFER_TIME,
                name=index_name(k),
                partialFilterExpression={"proof_status": {"$eq": k}},
            )


async def init_db():
    # must be idempotent
    db = client[settings.DB_NAME]
    ver_configs = db.get_collection(COLLECTION_NAMES.VER_CONFIGS)
    ver_configs.create_index([("ver_config_id", ASCENDING)], unique=True)

    client_configs = db.get_collection(COLLECTION_NAMES.CLIENT_CONFIGURATIONS)
    client_configs.create_index([("client_id", ASCENDING)], unique=True)

    auth_session = db.get_collection(COLLECTION_NAMES.AUTH_SESSION)
    auth_session.create_index([("pres_exch_id", ASCENDING)], unique=True)
    auth_session.create_index([("pyop_auth_code", ASCENDING)], unique=True)
    if settings.CONTROLLER_SESSION_TIMEOUT_CONFIG_FILE:
        create_ttl_indexes(
            auth_session, settings.CONTROLLER_SESSION_TIMEOUT_CONFIG_FILE
        )
    else:
        logger.warn(
            "No configuration file was set for CONTROLLER_SESSION_TIMEOUT_CONFIG_FILE"
            + " No expiration times will be applied.",
        )


async def get_db():
    return client[settings.DB_NAME]
