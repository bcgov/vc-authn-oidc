import uuid
from typing import Dict
from datetime import datetime, timedelta
from pydantic import BaseModel, Field


from api.core.models import UUIDModel
from api.core.acapy.client import AcapyClient
from bson import ObjectId

prefix = "auth_sess"


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class AuthSessionBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    pres_exch_id: uuid.UUID
    expired_timestamp: datetime = Field(default=datetime.now() + timedelta(seconds=600))
    ver_config_id: str
    request_parameters: dict

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class AuthSession(AuthSessionBase, UUIDModel):
    verified: bool = Field(default=False)

    @property
    def presentation_exchange(self) -> Dict:
        client = AcapyClient()
        return client.get_presentation_request(self.pres_exch_id)


class AuthSessionRead(AuthSessionBase):
    pass


class AuthSessionCreate(AuthSessionBase):
    pass


class AuthSessionPatch(AuthSessionBase):
    pass
