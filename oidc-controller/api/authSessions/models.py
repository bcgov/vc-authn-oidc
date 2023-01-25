import uuid
from typing import Dict
from datetime import datetime, timedelta

from sqlmodel import Field
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import JSON, UUID

from api.core.models import UUIDModel, BaseSQLModel
from api.core.acapy.client import AcapyClient

prefix = "auth_sess"


class AuthSessionBase(BaseSQLModel):
    expired_timestamp: datetime = Field(
        nullable=False, default=datetime.now() + timedelta(seconds=600)
    )  # only lasts 5 minutes
    ver_config_id: str = Field(nullable=False)
    pres_exch_id: uuid.UUID = Field(UUID(as_uuid=True), nullable=False)
    request_parameters: dict = Field(default={}, sa_column=Column(JSON))
    verified: bool = Field(nullable=False, default=False)


class AuthSession(AuthSessionBase, UUIDModel, table=True):
    __tablename__ = f"{prefix}_auth_sessions"

    @property
    def presentation_exchange(self) -> Dict:
        client = AcapyClient()
        return client.get_presentation_request(self.pres_exch_id)


class AuthSessionRead(AuthSessionBase, UUIDModel):
    pass


class AuthSessionCreate(AuthSessionBase):
    pass


class AuthSessionPatch(AuthSessionBase):
    pass
