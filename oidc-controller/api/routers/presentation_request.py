import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_async_session

from ..authSessions.models import AuthSession
from ..authSessions.crud import AuthSessionCRUD
from ..core.acapy.client import AcapyClient

from ..core.aries import (
    PresentationRequestMessage,
    ServiceDecorator,
    PresentProofv10Attachment,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/url/pres_exch/{pres_exch_id}")
async def send_connectionless_proof_req(
    pres_exch_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """QR code that is generated should a url to this endpoint, which responds with the
    specific payload for that given agent/wallet"""
    auth_sessions = AuthSessionCRUD(session)
    auth_session: AuthSession = await auth_sessions.get_by_pres_exch_id(pres_exch_id)
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
        service=s_d,
    )

    return JSONResponse(msg.dict(by_alias=True))
