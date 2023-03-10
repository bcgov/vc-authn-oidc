import pytest

from api.verificationConfigs.crud import VerificationConfigCRUD
from api.verificationConfigs.models import VerificationConfig, VerificationProofRequest
from mongomock import MongoClient
from typing import Callable


def test_answer():
    assert True


@pytest.mark.asyncio
async def test_ver_config_get(db_client: Callable[[], MongoClient]):
    test_ver_config = VerificationConfig(
        ver_config_id="test_ver_config",
        subject_identifier="test_sub_id",
        proof_request=VerificationProofRequest(
            version="0.0.1", requested_attributes=[], requested_predicates=[]
        ),
    )

    db_client().db.ver_configs.insert_one(test_ver_config.dict())
    result = await VerificationConfigCRUD(db_client).get("test_ver_config")
    assert result
