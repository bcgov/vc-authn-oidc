from pymongo import MongoClient, ASCENDING, database
from api.core.config import settings
from .collections import COLLECTION_NAMES


async def get_async_session():
    yield None


async def get_db() -> database.Database:
    client = MongoClient(settings.MONGODB_URL, uuidRepresentation="standard")
    db = client[settings.DB_NAME]

    ver_configs = db.get_collection(COLLECTION_NAMES.VER_CONFIGS)

    # idempotent
    ver_configs.create_index([("ver_config_id", ASCENDING)], unique=True)

    yield client.db
    client.close()
