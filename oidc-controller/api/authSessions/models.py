from datetime import datetime, timedelta
from enum import StrEnum, auto
from typing import Dict, Union

from api.core.acapy.client import AcapyClient
from api.core.models import UUIDModel
from pydantic import BaseModel, Field


class AuthSessionState(StrEnum):
    NOT_STARTED = auto()
    PENDING = auto()
    EXPIRED = auto()
    VERIFIED = auto()
    FAILED = auto()

class AuthSessionBase(BaseModel):
    pres_exch_id: str
    expired_timestamp: datetime = Field(default=datetime.now() + timedelta(seconds=600))
    ver_config_id: str
    request_parameters: dict
    pyop_auth_code: str
    response_url: str

    class Config:
        allow_population_by_field_name = True


class AuthSession(AuthSessionBase, UUIDModel):
    proof_status: AuthSessionState = Field(default=AuthSessionState.NOT_STARTED)
    proof_expired_time: Union[datetime, None] = Field(default=None)

    @property
    def presentation_exchange(self) -> Dict:
        client = AcapyClient()
        return client.get_presentation_request(self.pres_exch_id)


class AuthSessionCreate(AuthSessionBase):
    pass


class AuthSessionPatch(AuthSessionBase):
    proof_status: AuthSessionState = Field(default=AuthSessionState.PENDING)
    proof_expired_time: Union[datetime, None] = Field(default=None)
    pass
