import uuid
from datetime import datetime, timedelta

from sqlmodel import Field
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import JSON, UUID

from api.core.models import UUIDModel, BaseSQLModel


prefix = "auth_sess"


class AuthSessionBase(BaseSQLModel):
    expired_timestamp: datetime = Field(
        nullable=False, default=datetime.now() + timedelta(seconds=600)
    )  # only lasts 5 minutes
    ver_config_id: str = Field(nullable=False)
    pres_exch_id: uuid.UUID = Field(UUID(as_uuid=True), nullable=False)
    presentation_exchange: dict = Field(default={}, sa_column=Column(JSON))
    request_parameters: dict = Field(default={}, sa_column=Column(JSON))
    verified: bool = Field(nullable=False, default=False)


class AuthSession(AuthSessionBase, UUIDModel, table=True):
    __tablename__ = f"{prefix}_auth_sessions"


class AuthSessionRead(AuthSessionBase, UUIDModel):
    pass


class AuthSessionCreate(AuthSessionBase):
    pass


class AuthSessionPatch(AuthSessionBase):
    pass
