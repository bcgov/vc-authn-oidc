import logging
import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..authSessions.crud import AuthSessionCRUD
from ..authSessions.models import AuthSession
from ..core.acapy.client import AcapyClient
from ..core.aries import (
    PresentationRequestMessage,
    PresentProofv10Attachment,
    ServiceDecorator,
    OutOfBandMessage,
    OutOfBandPresentProofAttachment,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/url/pres_exch/{pres_exch_id}")
async def send_connectionless_proof_req(
    pres_exch_id: str,
):
    """QR code that is generated should a url to this endpoint, which responds with the
    specific payload for that given agent/wallet"""
    auth_session: AuthSession = await AuthSessionCRUD.get_by_pres_exch_id(pres_exch_id)
    client = AcapyClient()

    public_did = client.get_wallet_public_did()

    s_d = ServiceDecorator(
        service_endpoint=client.service_endpoint, recipient_keys=[public_did.verkey]
    )

    # bundle everything needed for the QR code
    byo_attachment = PresentProofv10Attachment.build(
        auth_session.presentation_exchange["presentation_request"]
    )

    # TODO Change this message type to OOB Protocol.
    msg = PresentationRequestMessage(
        id=auth_session.presentation_exchange["thread_id"],
        request=[byo_attachment],
        # service=s_d,
    )

    oob_msg = OutOfBandMessage(
        request_attachments=[
            OutOfBandPresentProofAttachment(
                id="request-0",
                data={"json": msg.dict(by_alias=True)},
            )
        ],
        id=auth_session.presentation_exchange["thread_id"],
        services=["did:sov:" + public_did.did],
    )
    print(json.dumps(oob_msg.dict(by_alias=True)))
    return JSONResponse(oob_msg.dict(by_alias=True))
    return JSONResponse(msg.dict(by_alias=True))


{
    "@id": "9c34c12d-2e64-42ce-af75-83712eee1d58",
    "@type": "https://didcomm.org/out-of-band/1.1/invitation",
    "goal_code": "request-proof",
    "requests~attach": [
        {
            "@id": "request-0",
            "mime-type": "application/json",
            "data": {
                "json": '{"id": "9c34c12d-2e64-42ce-af75-83712eee1d58", "type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation", "request": [{"id": "libindy-request-presentation-0", "mime_type": "application/json", "data": {"base64": "eyJub25jZSI6ICI4MTIxMzQ0ODA0MjQzMjA0Mjk3MTQ5MzYiLCAibmFtZSI6ICJwcm9vZl9yZXF1ZXN0ZWQiLCAidmVyc2lvbiI6ICIwLjAuMSIsICJyZXF1ZXN0ZWRfYXR0cmlidXRlcyI6IHsicmVxX2F0dHJfMCI6IHsibmFtZSI6ICJmaXJzdF9uYW1lIiwgInJlc3RyaWN0aW9ucyI6IFtdfSwgInJlcV9hdHRyXzEiOiB7Im5hbWUiOiAibGFzdF9uYW1lIiwgInJlc3RyaWN0aW9ucyI6IFtdfX0sICJyZXF1ZXN0ZWRfcHJlZGljYXRlcyI6IHt9fQ=="}}], "comment": null, "service": {"recipient_keys": ["8NmsVreo9UtPx1NSugqhrnPrDeZtUVHemwpDQBBzqQuE"], "routing_keys": null, "service_endpoint": "https://f0ff-165-225-211-69.ngrok.io"}}'
            },
        }
    ],
    "services": ["did:sov:EXrhGcG9VYSV2QA8m66B3P"],
}
