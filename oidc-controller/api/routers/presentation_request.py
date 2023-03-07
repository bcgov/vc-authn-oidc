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
from ..core.config import settings

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

    byo_attachment = PresentProofv10Attachment.build(
        auth_session.presentation_exchange["presentation_request"]
    )

    msg = None
    if settings.USE_OOB_PRESENT_PROOF:
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
        msg_contents = oob_msg
    else:
        s_d = ServiceDecorator(
            service_endpoint=client.service_endpoint, recipient_keys=[public_did.verkey]
        )
        msg = PresentationRequestMessage(
            id=auth_session.presentation_exchange["thread_id"],
            request=[byo_attachment],
            service=s_d,
        )
        msg_contents = msg
    print(msg_contents.dict(by_alias=True))
    return JSONResponse(msg_contents.dict(by_alias=True))
