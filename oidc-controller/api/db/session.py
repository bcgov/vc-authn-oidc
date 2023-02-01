from pymongo import MongoClient, ASCENDING
from api.core.config import settings
from .collections import COLLECTIONS


async def get_async_session():
    yield None


client = MongoClient(settings.DB_URL)
db = client[settings.PSQL_DB]


ver_configs = db.get_collection(COLLECTIONS.VER_CONFIGS)

# idempotent
ver_configs.create_index([("ver_config_id", ASCENDING)], unique=True)
