import json
import logging

from fastapi import APIRouter, Depends, Request
from pymongo.database import Database

from ..authSessions.crud import AuthSessionCRUD
from ..authSessions.models import (AuthSession, AuthSessionPatch,
                                   AuthSessionState)
from ..core.acapy.client import AcapyClient
from ..db.session import get_db

from ..core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


async def _parse_webhook_body(request: Request):
    return json.loads((await request.body()).decode("ascii"))


@router.post("/topic/{topic}/")
async def post_topic(request: Request, topic: str, db: Database = Depends(get_db)):
    """Called by aca-py agent."""
    logger.info(f">>> post_topic : topic={topic}")
    client = AcapyClient()
    match topic:
        case "present_proof":
            webhook_body = await _parse_webhook_body(request)
            print('webhook_body', webhook_body)
            print('created_at', webhook_body.get('created_at'))
            print('timeout value', settings.CONTROLLER_PRESENTATION_EXPIRE_TIME)
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
                auth_session.proof_status = AuthSessionState.VERIFIED if webhook_body["verified"] == "true" else AuthSessionState.FAILED
                await AuthSessionCRUD(db).patch(
                    str(auth_session.id), AuthSessionPatch(**auth_session.dict())
                )

            pass
        case _:
            logger.debug("skipping webhook")

    return {}
