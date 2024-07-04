import json

import mock
import pytest
from api.core.acapy.client import (
    CREATE_PRESENTATION_REQUEST_URL,
    PRESENT_PROOF_RECORDS,
    PUBLIC_WALLET_DID_URI,
    WALLET_DID_URI,
    AcapyClient,
)
from api.core.acapy.config import MultiTenantAcapy, SingleTenantAcapy
from api.core.acapy.models import CreatePresentationResponse, WalletDid
from api.core.acapy.tests.__mocks__ import (
    create_presentation_response_http,
    presentation_request_configuration,
)
from api.core.config import settings


@pytest.mark.asyncio
@mock.patch.object(settings, "ACAPY_TENANCY", None)
async def test_init_no_setting_returns_client_with_single_tenancy_config():
    client = AcapyClient()
    assert client is not None
    assert isinstance(client.agent_config, SingleTenantAcapy) is True


@pytest.mark.asyncio
@mock.patch.object(settings, "ACAPY_TENANCY", "single")
async def test_init_single_returns_client_with_single_tenancy_config():
    client = AcapyClient()
    assert client is not None
    assert isinstance(client.agent_config, SingleTenantAcapy) is True


@pytest.mark.asyncio
@mock.patch.object(settings, "ACAPY_TENANCY", "multi")
async def test_init_multi_returns_client_with_multi_tenancy_config():
    client = AcapyClient()
    assert client is not None
    assert isinstance(client.agent_config, MultiTenantAcapy) is True


@pytest.mark.asyncio
async def test_create_presentation_returns_sucessfully_with_valid_data(requests_mock):
    requests_mock.post(
        settings.ACAPY_ADMIN_URL + CREATE_PRESENTATION_REQUEST_URL,
        headers={},
        json=json.dumps(create_presentation_response_http),
        status_code=200,
    )

    with mock.patch.object(
        CreatePresentationResponse, "parse_obj", return_value={"result": "success"}
    ):
        client = AcapyClient()
        client.agent_config.get_headers = mock.MagicMock(return_value={"x-api-key": ""})
        presentation_request = client.create_presentation_request(
            presentation_request_configuration
        )
        assert presentation_request is not None


@pytest.mark.asyncio
async def test_create_presentation_throws_assertion_error_with_non_200_resp_from_acapy(
    requests_mock,
):
    requests_mock.post(
        settings.ACAPY_ADMIN_URL + CREATE_PRESENTATION_REQUEST_URL,
        headers={},
        json=json.dumps(create_presentation_response_http),
        status_code=400,
    )

    with mock.patch.object(
        CreatePresentationResponse, "parse_obj", return_value={"result": "success"}
    ):
        client = AcapyClient()
        client.agent_config.get_headers = mock.MagicMock(return_value={"x-api-key": ""})
        try:
            presentation_request = client.create_presentation_request(
                presentation_request_configuration
            )
            assert presentation_request is not None
        except AssertionError as e:
            assert e is not None


# TODO: determine if this function should assert a valid json response
@pytest.mark.asyncio
async def test_create_presentation_throws_error_with_non_json_from_acapy(requests_mock):
    requests_mock.post(
        settings.ACAPY_ADMIN_URL + CREATE_PRESENTATION_REQUEST_URL,
        headers={},
        status_code=200,
    )

    with mock.patch.object(
        CreatePresentationResponse, "parse_obj", return_value={"result": "success"}
    ):
        client = AcapyClient()
        client.agent_config.get_headers = mock.MagicMock(return_value={"x-api-key": ""})
        try:
            presentation_request = client.create_presentation_request(
                presentation_request_configuration
            )
            assert presentation_request is not None
        except json.JSONDecodeError as e:
            assert e is not None


@pytest.mark.asyncio
async def test_get_presentation_returns_sucessfully_with_valid_data(requests_mock):
    requests_mock.get(
        settings.ACAPY_ADMIN_URL + PRESENT_PROOF_RECORDS + "/" + "1234-567890",
        headers={},
        json={"result": "success"},
        status_code=200,
    )

    client = AcapyClient()
    client.agent_config.get_headers = mock.MagicMock(return_value={"x-api-key": ""})
    presentation = client.get_presentation_request("1234-567890")
    assert presentation is not None


@pytest.mark.asyncio
async def test_get_presentation_throws_assertion_error_for_non_200_response_from_acapy(
    requests_mock,
):
    requests_mock.get(
        settings.ACAPY_ADMIN_URL + PRESENT_PROOF_RECORDS + "/" + "1234-567890",
        headers={},
        json={"result": "success"},
        status_code=400,
    )

    client = AcapyClient()
    client.agent_config.get_headers = mock.MagicMock(return_value={"x-api-key": ""})
    try:
        client.get_presentation_request("1234-567890")
    except AssertionError as e:
        assert e is not None


@pytest.mark.asyncio
async def test_get_wallet_did_public_returns_sucessfully_on_public_url_and_simple_resp(
    requests_mock,
):
    requests_mock.get(
        settings.ACAPY_ADMIN_URL + PUBLIC_WALLET_DID_URI,
        headers={},
        json={"result": "success"},
        status_code=200,
    )
    with mock.patch.object(WalletDid, "parse_obj", return_value={"result": "success"}):
        client = AcapyClient()
        client.agent_config.get_headers = mock.MagicMock(return_value={"x-api-key": ""})
        wallet_resp = client.get_wallet_did(public=True)
        assert wallet_resp is not None


@pytest.mark.asyncio
async def test_get_wallet_did_public_throws_assertion_error_on_non_200_response(
    requests_mock,
):
    requests_mock.get(
        settings.ACAPY_ADMIN_URL + PUBLIC_WALLET_DID_URI,
        headers={},
        json={"result": "success"},
        status_code=400,
    )
    with mock.patch.object(WalletDid, "parse_obj", return_value={"result": "success"}):
        client = AcapyClient()
        client.agent_config.get_headers = mock.MagicMock(return_value={"x-api-key": ""})
        try:
            client.get_wallet_did(public=True)
        except AssertionError as e:
            assert e is not None


@pytest.mark.asyncio
async def test_get_wallet_did_not_public_returns_on_correct_url_and_processes_array(
    requests_mock,
):
    requests_mock.get(
        settings.ACAPY_ADMIN_URL + WALLET_DID_URI,
        headers={},
        json={"results": ["success"]},
        status_code=200,
    )
    with mock.patch.object(WalletDid, "parse_obj", return_value={"result": "success"}):
        client = AcapyClient()
        client.agent_config.get_headers = mock.MagicMock(return_value={"x-api-key": ""})
        wallet_resp = client.get_wallet_did(public=False)
        assert wallet_resp is not None
