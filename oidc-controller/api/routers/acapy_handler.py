import json
import logging

from fastapi import APIRouter, Request

from ..authSessions.crud import AuthSessionCRUD
from ..authSessions.models import AuthSession, AuthSessionPatch
from ..core.acapy.client import AcapyClient

logger = logging.getLogger(__name__)

router = APIRouter()


async def _parse_webhook_body(request: Request):
    return json.loads((await request.body()).decode("ascii"))


@router.post("/topic/{topic}/")
async def post_topic(
    request: Request,
    topic: str,
):
    """Called by aca-py agent."""
    logger.info(f">>> post_topic : topic={topic}")
    client = AcapyClient()
    match topic:
        case "present_proof":
            webhook_body = await _parse_webhook_body(request)
            logger.info(
                f">>>> pres_exch_id: {webhook_body['presentation_exchange_id']}"
            )
            auth_session: AuthSession = await AuthSessionCRUD.get_by_pres_exch_id(
                webhook_body["presentation_exchange_id"]
            )
            if webhook_body["state"] == "presentation_received":
                logger.info("GOT A PRESENTATION, TIME TO VERIFY")
                client.verify_presentation(auth_session.pres_exch_id)
            if webhook_body["state"] == "verified":
                logger.info("VERIFIED")
                # update presentation_exchange record
                auth_session.verified = True
                await AuthSessionCRUD.patch(
                    auth_session.id, AuthSessionPatch(**auth_session.dict())
                )

            pass
        case _:
            logger.debug("skipping webhook")

    return {}
