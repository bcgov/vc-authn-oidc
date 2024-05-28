import json
from pymongo import MongoClient, ASCENDING
from pathlib import Path
from api.core.config import settings
from .collections import COLLECTION_NAMES
from ..core.config import settings
from ..authSessions.models import AuthSessionState


async def get_async_session():
    yield None


client = MongoClient(settings.MONGODB_URL, uuidRepresentation="standard")


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

    with open(
        (
            Path(__file__).parent.parent / "authSessions" / "sessiontimeout.json"
        ).resolve()
    ) as user_file:
        experation_times: dict[str, int] = json.loads(user_file.read())
        auth_session_states: list[str] = [str(i) for i in list(AuthSessionState)]
        for k, v in experation_times.items():
            assert isinstance(k, str)
            assert k in auth_session_states
            auth_session.create_index(
                [("created_at", ASCENDING)],
                expireAfterSeconds=v + settings.CONTROLLER_PRESENTATION_BUFFER_TIME,
                name=k + "_ttl",
                partialFilterExpression={"proof_status": {"$eq": k}},
            )


async def get_db():
    return client[settings.DB_NAME]
