import requests, json

acapy_traction_host: str = ""
wallet_name: str
wallet_webhook_url: str = "http://controller:5000/webhooks"
ledger_register_url: str = "http://test.bcovrin.vonx.io/register"
acapy_x_api_key: str = "change-me"


create_wallet_response: dict = {}
create_did_response: dict = {}
wallet_token: str = None

if not acapy_traction_host:
    print("USING DEFAULT DEVELOPMENT URL")
    acapy_traction_host = "http://localhost:8031"


print(f"acapy_traction_host={acapy_traction_host}")
print(f"wallet_webhook_url={wallet_webhook_url}")
print(f"ledger_register_url={ledger_register_url}")
input("Press any key to proceed, or CTRL-C to cancel")

wallet_payload = {
    "key_management_mode": "managed",
    "label": "vc-authn-oidc-dev",
    "wallet_name": "vc-authn-oidc-dev-wallet",
    "wallet_type": "askar",
    "wallet_webhook_urls": [wallet_webhook_url],
}


def create_wallet():
    print(">>> create_wallet")
    resp_raw = requests.post(
        acapy_traction_host + "/multitenancy/wallet",
        headers={"x-api-key": acapy_x_api_key},
        json=wallet_payload,
    )
    assert resp_raw.status_code == 200, resp_raw.content

    global create_wallet_response
    create_wallet_response = json.loads(resp_raw.content)


def get_wallet_token():
    print(">>> create_did")
    resp_raw = requests.post(
        acapy_traction_host
        + "/multitenancy/wallet/"
        + create_wallet_response["wallet_id"]
        + "/token",
        headers={"x-api-key": acapy_x_api_key},
    )
    assert resp_raw.status_code == 200, resp_raw.content

    global wallet_token
    wallet_token = json.loads(resp_raw.content)["token"]


def create_did():
    print(">>> create_did")

    global wallet_token
    if not wallet_token:
        get_wallet_token()

    resp_raw = requests.post(
        acapy_traction_host + "/wallet/did/create",
        headers={
            "x-api-key": acapy_x_api_key,
            "Authorization": "Bearer " + wallet_token,
        },
    )
    assert resp_raw.status_code == 200, resp_raw.content

    global create_did_response
    create_did_response = json.loads(resp_raw.content)["result"]


def publish_did_to_ledger():
    print(">>> publish_did_to_ledger")
    global create_did_response

    resp_raw = requests.post(
        ledger_register_url,
        json={
            "alias": "vc-authn-oidc-dev-did",
            "did": create_did_response["did"],
            "verkey": create_did_response["verkey"],
            "role": "ENDORSER",
        },
    )
    assert resp_raw.status_code == 200, resp_raw.content


def set_did_as_public():
    print(">>> set_did_as_public")

    global wallet_token
    if not wallet_token:
        get_wallet_token()

    resp_raw = requests.post(
        acapy_traction_host + "/wallet/did/public",
        headers={
            "x-api-key": acapy_x_api_key,
            "Authorization": "Bearer " + wallet_token,
        },
        params={"did": create_did_response["did"]},
    )
    assert resp_raw.status_code == 200, resp_raw.content


if __name__ == "__main__":
    create_wallet()
    create_did()
    publish_did_to_ledger()
    set_did_as_public()

    print(
        f"wallet_id={create_wallet_response['wallet_id']} and public did created successfully."
    )
    print(
        f"set ACAPY_WALLET_ID to {create_wallet_response['wallet_id']} in /scripts/.env and then run 'docker-compose up'"
    )
