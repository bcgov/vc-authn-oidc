import base64
import io
import structlog
from urllib.parse import urlencode
from datetime import datetime

import qrcode
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from jinja2 import Template
from oic.oic.message import AccessTokenRequest, AuthorizationRequest
from pymongo.database import Database

from ..authSessions.crud import AuthSessionCreate, AuthSessionCRUD
from ..authSessions.models import AuthSessionState, AuthSessionPatch
from ..core.acapy.client import AcapyClient
from ..core.config import settings
from ..core.logger_util import log_debug
from ..core.oidc import provider
from ..core.oidc.issue_token_service import Token
from ..db.session import get_db
from ..verificationConfigs.crud import VerificationConfigCRUD

# This allows the templates to insert assets like css, js or svg.
from ..templates.helpers import add_asset

ChallengePollUri = "/poll"
AuthorizeCallbackUri = "/callback"
VerifiedCredentialAuthorizeUri = "/authorize"
VerifiedCredentialTokenUri = "/token"

logger: structlog.typing.FilteringBoundLogger = structlog.getLogger(__name__)

router = APIRouter()


@log_debug
@router.get(f"{ChallengePollUri}/{{pid}}")
async def poll_pres_exch_complete(pid: str, db: Database = Depends(get_db)):
    """Called by authorize webpage to see if request
    is verified and token issuance can proceed."""
    auth_session = await AuthSessionCRUD(db).get(pid)

    """
     Check if proof is expired. But only if the proof has not been started.
     NOTE: This should eventually be moved to a background task.
    """
    if (
        auth_session.expired_timestamp < datetime.now()
        and auth_session.proof_status == AuthSessionState.NOT_STARTED
    ):
        logger.info("PROOF EXPIRED")
        auth_session.proof_status = AuthSessionState.EXPIRED
        await AuthSessionCRUD(db).patch(
            str(auth_session.id), AuthSessionPatch(**auth_session.dict())
        )

    return {"proof_status": auth_session.proof_status}


@log_debug
@router.get(VerifiedCredentialAuthorizeUri, response_class=HTMLResponse)
async def get_authorize(request: Request, db: Database = Depends(get_db)):
    """Called by oidc platform."""
    logger.debug(">>> get_authorize")

    # Verify OIDC forward payload
    model = AuthorizationRequest().from_dict(request.query_params._dict)
    model.verify()

    auth_req = provider.provider.parse_authentication_request(
        urlencode(request.query_params._dict), request.headers
    )
    #  fetch placeholder user/model and create proof
    authn_response = provider.provider.authorize(model, "vc-user")

    # retrieve presentation_request config.
    client = AcapyClient()
    ver_config_id = model.get("pres_req_conf_id")
    ver_config = await VerificationConfigCRUD(db).get(ver_config_id)

    # Create presentation_request to show on screen
    response = client.create_presentation_request(ver_config.generate_proof_request())

    new_auth_session = AuthSessionCreate(
        response_url=authn_response.request(auth_req["redirect_uri"]),
        pyop_auth_code=authn_response["code"],
        request_parameters=model.to_dict(),
        ver_config_id=ver_config_id,
        pres_exch_id=response.presentation_exchange_id,
        presentation_exchange=response.dict(),
    )

    # save OIDC AuthSession
    auth_session = await AuthSessionCRUD(db).create(new_auth_session)

    # QR CONTENTS
    controller_host = settings.CONTROLLER_URL
    url_to_message = (
        controller_host + "/url/pres_exch/" + str(auth_session.pres_exch_id)
    )
    # CREATE the image
    buff = io.BytesIO()
    qrcode.make(url_to_message).save(buff, format="PNG")
    image_contents = base64.b64encode(buff.getvalue()).decode("utf-8")
    callback_url = f"""{controller_host}{AuthorizeCallbackUri}?pid={auth_session.id}"""

    # This is the payload to send to the template
    data = {
        "image_contents": image_contents,
        "url_to_message": url_to_message,
        "callback_url": callback_url,
        "add_asset": add_asset,
        "pres_exch_id": auth_session.pres_exch_id,
        "pid": auth_session.id,
        "controller_host": controller_host,
        "challenge_poll_uri": ChallengePollUri,
    }

    # Prepare the template
    template_file = open("api/templates/verified_credentials.html", "r").read()
    template = Template(template_file)

    # Render and return the template
    return template.render(data)


@log_debug
@router.get("/callback", response_class=RedirectResponse)
async def get_authorize_callback(pid: str, db: Database = Depends(get_db)):
    """Called by Authorize page when verification is complete"""
    auth_session = await AuthSessionCRUD(db).get(pid)

    url = auth_session.response_url
    return RedirectResponse(url)


@log_debug
@router.post(VerifiedCredentialTokenUri, response_class=JSONResponse)
async def post_token(request: Request, db: Database = Depends(get_db)):
    """Called by oidc platform to retrieve token contents"""
    form = await request.form()
    model = AccessTokenRequest().from_dict(form._dict)
    client = AcapyClient()

    auth_session = await AuthSessionCRUD(db).get_by_pyop_auth_code(model.get("code"))
    ver_config = await VerificationConfigCRUD(db).get(auth_session.ver_config_id)
    presentation = client.get_presentation_request(auth_session.pres_exch_id)
    claims = Token.get_claims(presentation, auth_session, ver_config)

    # modify subject identifier value to use vc-attribute as configured
    new_sub = claims.pop("sub")
    provider.provider.authz_state.authorization_codes[model.get("code")][
        "public"
    ] = new_sub

    # convert form data to what library expects, Flask.app.request.get_data()
    data = urlencode(form._dict)
    token_response = provider.provider.handle_token_request(
        data, request.headers, claims
    )
    return token_response.to_dict()
