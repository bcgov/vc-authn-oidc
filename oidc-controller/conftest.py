from api.core.config import settings

import pytest
import mongomock


@pytest.fixture()
def db_client():
    def get_mock_db_client() -> mongomock.MongoClient:
        return mongomock.MongoClient()

    return get_mock_db_client


@pytest.fixture()
def db(db_client):
    return db_client().db


settings.CONTROLLER_URL = "https://controller"
settings.SIGNING_KEY_FILENAME = "tests/test_signing_key.pem"
