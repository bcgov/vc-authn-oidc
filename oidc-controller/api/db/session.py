from pymongo import MongoClient, ASCENDING
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

    expire_time: int = settings.CONTROLLER_PRESENTATION_EXPIRE_TIME + settings.CONTROLLER_PRESENTATION_BUFFER_TIME

    for k, v in [("expired_ttl", AuthSessionState.EXPIRED),
                 ("failed_ttl", AuthSessionState.FAILED),
                 ("abandoned_ttl", AuthSessionState.ABANDONED)]:
        auth_session.create_index([("created_at", ASCENDING)],
                                  expireAfterSeconds=expire_time,
                                  name=k,
                                  partialFilterExpression={"proof_status":
                                                           { "$eq": v.value }})


async def get_db():
    return client[settings.DB_NAME]
