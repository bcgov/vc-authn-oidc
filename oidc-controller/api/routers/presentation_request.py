import structlog

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from jinja2 import Template
from pymongo.database import Database

from ..authSessions.crud import AuthSessionCRUD
from ..authSessions.models import AuthSession, AuthSessionState

from ..core.config import settings
from ..routers.socketio import sio, connections_reload
from ..db.session import get_db
from ..templates.helpers import add_asset

logger: structlog.typing.FilteringBoundLogger = structlog.getLogger(__name__)

router = APIRouter()


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
    if ".html" in settings.CONTROLLER_CAMERA_REDIRECT_URL:
        response = RedirectResponse(settings.CONTROLLER_CAMERA_REDIRECT_URL)
    else:
        template_file = open(
            f"api/templates/{settings.CONTROLLER_CAMERA_REDIRECT_URL}.html", "r"
        ).read()
        template = Template(template_file)
        response = HTMLResponse(template.render(data))

    if "text/html" in req.headers.get("accept"):
        logger.info("Redirecting to instructions page")
        return response

    auth_session: AuthSession = await AuthSessionCRUD(db).get_by_pres_exch_id(
        pres_exch_id
    )

    # Get the websocket session
    connections = connections_reload()
    sid = connections.get(str(auth_session.id))

    # If the qrcode has been scanned, toggle the verified flag
    if auth_session.proof_status is AuthSessionState.NOT_STARTED:
        auth_session.proof_status = AuthSessionState.PENDING
        await AuthSessionCRUD(db).patch(auth_session.id, auth_session)
        await sio.emit("status", {"status": "pending"}, to=sid)

    msg = auth_session.presentation_request_msg

    logger.debug(msg)
    return JSONResponse(msg)
