import pytest

from api.clientConfigurations.crud import ClientConfigurationCRUD
from api.clientConfigurations.models import (
    ClientConfiguration,
    ClientConfigurationPatch,
)

from api.db.session import COLLECTION_NAMES

from mongomock import MongoClient
from typing import Callable


def test_answer():
    assert True


test_client_config = ClientConfiguration(
    client_id="test_client",
    client_name="test_client_name",
    client_secret="test_client_secret",
    redirect_uris=["http://redirecturi.com"],
)


@pytest.mark.asyncio
async def test_client_config_get(db_client: Callable[[], MongoClient]):
    client = db_client()
    crud = ClientConfigurationCRUD(client.db)

    client.db.get_collection(COLLECTION_NAMES.CLIENT_CONFIGURATIONS).insert_one(
        test_client_config.dict()
    )

    result = await crud.get(test_client_config.client_id)
    assert result


@pytest.mark.asyncio
async def test_client_config_create(db_client: Callable[[], MongoClient]):
    client = db_client()
    crud = ClientConfigurationCRUD(client.db)

    await crud.create(test_client_config)
    document = client.db.get_collection(
        COLLECTION_NAMES.CLIENT_CONFIGURATIONS
    ).find_one({"client_id": test_client_config.client_id})
    assert document


@pytest.mark.asyncio
async def test_client_config_delete(db_client: Callable[[], MongoClient]):
    client = db_client()
    crud = ClientConfigurationCRUD(client.db)

    client.db.get_collection(COLLECTION_NAMES.CLIENT_CONFIGURATIONS).insert_one(
        test_client_config.dict()
    )

    result = await crud.delete(test_client_config.client_id)
    assert result

    document = client.db.get_collection(
        COLLECTION_NAMES.CLIENT_CONFIGURATIONS
    ).find_one({"client_id": test_client_config.client_id})
    assert not document


@pytest.mark.asyncio
async def test_client_config_patch(db_client: Callable[[], MongoClient]):
    client = db_client()
    crud = ClientConfigurationCRUD(client.db)

    client.db.get_collection(COLLECTION_NAMES.CLIENT_CONFIGURATIONS).insert_one(
        test_client_config.dict()
    )

    result = await crud.patch(
        test_client_config.client_id,
        ClientConfigurationPatch(client_secret="patched_client_secret"),
    )
    assert result

    document = client.db.get_collection(
        COLLECTION_NAMES.CLIENT_CONFIGURATIONS
    ).find_one({"client_id": test_client_config.client_id})
    assert document["client_secret"] == "patched_client_secret"
