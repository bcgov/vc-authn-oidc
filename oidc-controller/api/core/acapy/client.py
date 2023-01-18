import requests
import json
import logging
from uuid import UUID

from .models import WalletPublicDid, CreatePresentationResponse
from ..config import settings

_client = None
logger = logging.getLogger(__name__)

WALLET_DID_URI = "/wallet/did/public"
CREATE_PRESENTATION_REQUEST_URL = "/present-proof/create-request"
PRESENT_PROOF_RECORDS = "/present-proof/records"


class AcapyClient:
    wallet_id = settings.ACAPY_WALLET_ID
    wallet_key = settings.ACAPY_WALLET_KEY
    acapy_host = settings.ACAPY_ADMIN_URL
    acapy_admin_api_key = settings.ACAPY_ADMIN_URL_API_KEY
    service_endpoint = settings.ACAPY_AGENT_URL

    wallet_token: str = None

    def __init__(self):
        if _client:
            return _client
        super().__init__()

    def get_wallet_token(self):
        logger.debug(f">>> get_wallet_token")
        resp_raw = requests.post(
            self.acapy_host + f"/multitenancy/wallet/{self.wallet_id}/token",
            json={"wallet_key": self.wallet_key},
            headers={settings.ACAPY_WEBHOOK_URL_API_KEY_NAME: self.acapy_admin_api_key},
        )
        assert (
            resp_raw.status_code == 200
        ), f"{resp_raw.status_code}::{resp_raw.content}"
        resp = json.loads(resp_raw.content)
        self.wallet_token = resp["token"]
        logger.debug(f"<<< get_wallet_token")

        return self.wallet_token

    def create_presentation_request(
        self, presentation_request_configuration: dict
    ) -> CreatePresentationResponse:
        logger.debug(f">>> create_presentation_request")
        if not self.wallet_token:
            self.get_wallet_token()

        present_proof_payload = {"proof_request": presentation_request_configuration}

        resp_raw = requests.post(
            self.acapy_host + CREATE_PRESENTATION_REQUEST_URL,
            headers={
                settings.ACAPY_WEBHOOK_URL_API_KEY_NAME: self.acapy_admin_api_key,
                "Authorization": "Bearer " + self.wallet_token,
            },
            json=present_proof_payload,
        )
        assert resp_raw.status_code == 200, resp_raw.content
        resp = json.loads(resp_raw.content)
        result = CreatePresentationResponse.parse_obj(resp)

        logger.debug(f"<<< create_presenation_request")
        return result

    def get_presentation_request(self, presentation_exchange_id: UUID):
        logger.debug(f">>> get_presentation_request")
        if not self.wallet_token:
            self.get_wallet_token()

        resp_raw = requests.get(
            self.acapy_host
            + PRESENT_PROOF_RECORDS
            + "/"
            + str(presentation_exchange_id),
            headers={
                settings.ACAPY_WEBHOOK_URL_API_KEY_NAME: self.acapy_admin_api_key,
                "Authorization": "Bearer " + self.wallet_token,
            },
        )
        assert resp_raw.status_code == 200, resp_raw.content
        resp = json.loads(resp_raw.content)

        logger.debug(f"<<< get_presentation_request -> {resp}")
        return resp

    def verify_presentation(self, presentation_exchange_id: UUID):
        logger.debug(f">>> verify_presentation")
        if not self.wallet_token:
            self.get_wallet_token()

        resp_raw = requests.post(
            self.acapy_host
            + PRESENT_PROOF_RECORDS
            + "/"
            + str(presentation_exchange_id)
            + "/verify-presentation",
            headers={
                settings.ACAPY_WEBHOOK_URL_API_KEY_NAME: self.acapy_admin_api_key,
                "Authorization": "Bearer " + self.wallet_token,
            },
        )
        assert resp_raw.status_code == 200, resp_raw.content
        resp = json.loads(resp_raw.content)

        logger.debug(f"<<< verify_presentation -> {resp}")
        return resp

    def get_wallet_public_did(self) -> WalletPublicDid:
        logger.debug(f">>> get_wallet_public_did")

        if not self.wallet_token:
            self.get_wallet_token()
        resp_raw = requests.get(
            self.acapy_host + WALLET_DID_URI,
            headers={
                settings.ACAPY_WEBHOOK_URL_API_KEY_NAME: self.acapy_admin_api_key,
                "Authorization": "Bearer " + self.wallet_token,
            },
        )
        assert (
            resp_raw.status_code == 200
        ), f"{resp_raw.status_code}::{resp_raw.content}"
        resp = json.loads(resp_raw.content)
        public_did = WalletPublicDid.parse_obj(resp["result"])

        logger.debug(f"<<< get_wallet_public_did -> {public_did}")
        return public_did
