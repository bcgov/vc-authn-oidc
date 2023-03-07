from typing import Optional, Dict

from pydantic import BaseModel, Field


class WalletDid(BaseModel):
    did: str
    verkey: str
    posture: str

class WalletDidPublicResponse(BaseModel):
    result: Optional[WalletDid]


class CreatePresentationResponse(BaseModel):
    thread_id: str
    presentation_exchange_id: str
    presentation_request: Dict
