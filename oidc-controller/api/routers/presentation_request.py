import logging

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from pymongo.database import Database

from ..authSessions.crud import AuthSessionCRUD
from ..authSessions.models import AuthSession
from ..core.acapy.client import AcapyClient
from ..core.aries import (
    PresentationRequestMessage,
    PresentProofv10Attachment,
    ServiceDecorator,
    OutOfBandMessage,
    OutOfBandPresentProofAttachment,
    OOBServiceDecorator,
)
from ..core.config import settings
from ..db.session import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/url/pres_exch/{pres_exch_id}")
async def send_connectionless_proof_req(
    pres_exch_id: str, req: Request, db: Database = Depends(get_db)
):
    """QR code that is generated should a url to this endpoint, which responds with the
    specific payload for that given agent/wallet"""

    """TODO: Check if this is coming from a browser
    If so, redirect to here https://id.gov.bc.ca/static/selfsetup.html
    """
    logger.info("Scanning Application headers:: " + str(req.headers))
    print("Application headers:: " + str(req.headers))
    print("Accept string:: " + req.headers.get('accept'))
    # if req.headers.get('accept') matches application/json then
    #   business as aways
    # else
    #   redirect to instructions page

    auth_session: AuthSession = await AuthSessionCRUD(db).get_by_pres_exch_id(
        pres_exch_id
    )
    client = AcapyClient()
    use_public_did = (
        not settings.USE_OOB_PRESENT_PROOF
    ) and settings.USE_OOB_LOCAL_DID_SERVICE
    wallet_did = client.get_wallet_did(public=use_public_did)

    byo_attachment = PresentProofv10Attachment.build(
        auth_session.presentation_exchange["presentation_request"]
    )

    msg = None
    if settings.USE_OOB_PRESENT_PROOF:
        if settings.USE_OOB_LOCAL_DID_SERVICE:
            oob_s_d = OOBServiceDecorator(
                service_endpoint=client.service_endpoint,
                recipient_keys=[wallet_did.verkey],
            ).dict()
        else:
            wallet_did = client.get_wallet_did(public=True)
            oob_s_d = wallet_did.verkey

        msg = PresentationRequestMessage(
            id=auth_session.presentation_exchange["thread_id"],
            request=[byo_attachment],
        )
        oob_msg = OutOfBandMessage(
            request_attachments=[
                OutOfBandPresentProofAttachment(
                    id="request-0",
                    data={"json": msg.dict(by_alias=True)},
                )
            ],
            id=auth_session.presentation_exchange["thread_id"],
            services=[oob_s_d],
        )
        msg_contents = oob_msg
    else:
        s_d = ServiceDecorator(
            service_endpoint=client.service_endpoint, recipient_keys=[wallet_did.verkey]
        )
        msg = PresentationRequestMessage(
            id=auth_session.presentation_exchange["thread_id"],
            request=[byo_attachment],
            service=s_d,
        )
        msg_contents = msg
    print(msg_contents.dict(by_alias=True))
    return JSONResponse(msg_contents.dict(by_alias=True))
