from pymongo import MongoClient, ASCENDING
from api.core.config import settings
from .collections import COLLECTION_NAMES


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

async def get_db():
    return client[settings.DB_NAME]
