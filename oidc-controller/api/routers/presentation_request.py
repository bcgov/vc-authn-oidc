import logging

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pymongo.database import Database
from jinja2 import Template

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

# Add assets to templates, like css, js or svg.
def add_asset(name):
    return open(f"api/templates/assets/{name}", "r").read()

@router.get("/url/pres_exch/{pres_exch_id}")
async def send_connectionless_proof_req(
    pres_exch_id: str, req: Request, db: Database = Depends(get_db)
):
    """
      If the user scanes the QR code with a mobile camera,
      they will be redirected to a help page.
    """
    data = {
        "add_asset": add_asset,
    }
    # First prepare the response depending on the redirect url
    if '.html' in settings.CONTROLLER_CAMERA_REDIRECT_URL:
        response = RedirectResponse(settings.CONTROLLER_CAMERA_REDIRECT_URL)
    else:
        template_file = open(f'api/templates/{settings.CONTROLLER_CAMERA_REDIRECT_URL}.html', "r").read()
        template = Template(template_file)
        response = HTMLResponse(template.render(data))

    if 'text/html' in req.headers.get('accept'):
        print("Redirecting to instructions page")
        return response

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
