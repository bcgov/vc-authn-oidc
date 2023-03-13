from typing import Optional, Dict

from pydantic import BaseModel


class WalletPublicDid(BaseModel):
    did: str
    verkey: str
    posture: str


class WalletDidPublicResponse(BaseModel):
    result: Optional[WalletPublicDid]


class CreatePresentationResponse(BaseModel):
    thread_id: str
    presentation_exchange_id: str
    presentation_request: Dict
