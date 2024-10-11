import requests
import structlog
import json

from functools import cache
from typing import Protocol

from ..config import settings

logger: structlog.typing.FilteringBoundLogger = structlog.getLogger(__name__)


class AgentConfig(Protocol):
    def get_headers() -> dict[str, str]: ...


class MultiTenantAcapy:
    wallet_id = settings.MT_ACAPY_WALLET_ID
    wallet_key = settings.MT_ACAPY_WALLET_KEY

    @cache
    def get_wallet_token(self):
        logger.debug(">>> get_wallet_token")
        resp_raw = requests.post(
            settings.ACAPY_ADMIN_URL + f"/multitenancy/wallet/{self.wallet_id}/token",
        )
        assert (
            resp_raw.status_code == 200
        ), f"{resp_raw.status_code}::{resp_raw.content}"
        resp = json.loads(resp_raw.content)
        wallet_token = resp["token"]
        logger.debug("<<< get_wallet_token")

        return wallet_token

    def get_headers(self) -> dict[str, str]:
        return {"Authorization": "Bearer " + self.get_wallet_token()}


class SingleTenantAcapy:
    def get_headers(self) -> dict[str, str]:
        return {settings.ST_ACAPY_ADMIN_API_KEY_NAME: settings.ST_ACAPY_ADMIN_API_KEY}
