from typing import Optional, Dict
from ..aries import OutOfBandMessage

from pydantic import BaseModel


class WalletDid(BaseModel):
    did: str
    verkey: str
    posture: str


class WalletDidPublicResponse(BaseModel):
    result: Optional[WalletDid] = None


class CreatePresentationResponse(BaseModel):
    thread_id: str
    pres_ex_id: str
    pres_request: Dict


class OobCreateInvitationResponse(BaseModel):
    invi_msg_id: str
    invitation_url: str
    oob_id: str
    trace: bool
    state: str
    invitation: OutOfBandMessage
