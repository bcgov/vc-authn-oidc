import mock
import pytest
from api.core.acapy.config import MultiTenantAcapy, SingleTenantAcapy
from api.core.config import settings


@pytest.mark.asyncio
@mock.patch.object(settings, "ST_ACAPY_ADMIN_API_KEY_NAME", 'name')
@mock.patch.object(settings, "ST_ACAPY_ADMIN_API_KEY", 'key')
async def test_single_tenant_has_expected_headers():
    acapy = SingleTenantAcapy()
    headers = acapy.get_headers()
    assert headers == {'name': 'key'}


@pytest.mark.asyncio
async def test_multi_tenant_get_headers_returns_bearer_token_auth(requests_mock):
    acapy = MultiTenantAcapy()
    acapy.get_wallet_token = mock.MagicMock(return_value='token')
    headers = acapy.get_headers()
    assert headers == {"Authorization": "Bearer token"}


@pytest.mark.asyncio
async def test_multi_tenant_get_wallet_token_returns_token_at_token_key(requests_mock):
    requests_mock.post(
        settings.ACAPY_ADMIN_URL + "/multitenancy/wallet/wallet_id/token",
        headers={},
        json={'token': 'token'},
        status_code=200,
    )
    acapy = MultiTenantAcapy()
    acapy.wallet_id = 'wallet_id'
    token = acapy.get_wallet_token()
    assert token == 'token'


@pytest.mark.asyncio
async def test_multi_tenant_throws_assertion_error_for_non_200_response(requests_mock):
    requests_mock.post(
        settings.ACAPY_ADMIN_URL + "/multitenancy/wallet/wallet_id/token",
        headers={},
        json={'token': 'token'},
        status_code=400,
    )
    acapy = MultiTenantAcapy()
    acapy.wallet_id = 'wallet_id'
    try:
        acapy.get_wallet_token()
    except AssertionError as e:
        assert e is not None
