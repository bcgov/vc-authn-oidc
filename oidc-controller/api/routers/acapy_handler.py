import json
import logging
from datetime import datetime, timedelta, timezone

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
            logger.info(
                f">>>> pres_exch_id: {webhook_body['presentation_exchange_id']}"
            )
            created_time = datetime.fromisoformat(webhook_body.get('created_at'))

            expired_time  = created_time + timedelta(seconds=settings.CONTROLLER_PRESENTATION_EXPIRE_TIME)
            now_time = datetime.now(timezone.utc)
            print('time difference', expired_time < now_time)
            # TODO: This logic should also be added to the polling logic
            # TODO: And possibly add the timeout value to the AuthSession model
            # print('time difference', expired_time > datetime.now())
            # calculate the number of seconds between two times
            # time_delta = datetime.now() - created_time
            # print('time_diff', time_delta.total_seconds())

            # print('expired_time', expired_time)

            print('timeout value', settings.CONTROLLER_PRESENTATION_EXPIRE_TIME)
            print('webhook_body', webhook_body)
            print('created_at', webhook_body.get('created_at'))
            print('now', datetime.now(timezone.utc))

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
