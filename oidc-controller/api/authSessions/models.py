from typing import Dict
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from api.core.models import UUIDModel
from api.core.acapy.client import AcapyClient


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
    verified: str = Field(default='New')
    # verified: bool = Field(default=False)

    @property
    def presentation_exchange(self) -> Dict:
        client = AcapyClient()
        return client.get_presentation_request(self.pres_exch_id)


class AuthSessionCreate(AuthSessionBase):
    pass


class AuthSessionPatch(AuthSessionBase):
    verified: bool = Field(default=False)
    pass
