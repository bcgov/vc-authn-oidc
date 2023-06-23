import json
import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request, WebSocket
from pymongo.database import Database

from ..authSessions.crud import AuthSessionCRUD
from ..authSessions.models import AuthSession, AuthSessionPatch, AuthSessionState
from ..core.acapy.client import AcapyClient
from ..db.session import get_db

from ..core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


async def _parse_webhook_body(request: Request):
    return json.loads((await request.body()).decode("ascii"))

# TODO: Add webook handler

@router.post("/topic/{topic}/")
async def post_topic(request: Request, topic: str, db: Database = Depends(get_db)):
    """Called by aca-py agent."""
    logger.info(f">>> post_topic : topic={topic}")
    client = AcapyClient()
    match topic:
        case "present_proof":
            webhook_body = await _parse_webhook_body(request)
            logger.info(
                f">>>> pres_exch_id: {webhook_body['presentation_exchange_id']}"
            )

            auth_session: AuthSession = await AuthSessionCRUD(db).get_by_pres_exch_id(
                webhook_body["presentation_exchange_id"]
            )

            if webhook_body["state"] == "presentation_received":
                logger.info("GOT A PRESENTATION, TIME TO VERIFY")
                client.verify_presentation(auth_session.pres_exch_id)
            if webhook_body["state"] == "verified":
                logger.info("VERIFIED")
                # update auth session record with verification result
                auth_session.proof_status = (
                    AuthSessionState.VERIFIED
                    if webhook_body["verified"] == "true"
                    else AuthSessionState.FAILED
                )
                await AuthSessionCRUD(db).patch(
                    str(auth_session.id), AuthSessionPatch(**auth_session.dict())
                )

            # Calcuate the expiration time of the proof
            now_time = datetime.now()
            expired_time = now_time + timedelta(
                seconds=settings.CONTROLLER_PRESENTATION_EXPIRE_TIME
            )

            # Update the expiration time of the proof
            auth_session.expired_timestamp = expired_time
            await AuthSessionCRUD(db).patch(
                str(auth_session.id), AuthSessionPatch(**auth_session.dict())
            )

            # Check if expired. But only if the proof has not been started.
            if (
                expired_time < now_time
                and auth_session.proof_status == AuthSessionState.NOT_STARTED
            ):
                logger.info("EXPIRED")
                auth_session.proof_status = AuthSessionState.EXPIRED
                await AuthSessionCRUD(db).patch(
                    str(auth_session.id), AuthSessionPatch(**auth_session.dict())
                )

            pass
        case _:
            logger.debug("skipping webhook")

    return {}
