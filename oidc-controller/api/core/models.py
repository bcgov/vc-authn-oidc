from datetime import datetime
from typing import TypedDict

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from pyop.userinfo import Userinfo


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
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class HealthCheck(BaseModel):
    name: str
    version: str
    description: str


class StatusMessage(BaseModel):
    status: bool
    message: str


class UUIDModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(json_encoders={ObjectId: str})


class TimestampModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class GenericErrorMessage(BaseModel):
    detail: str


# Currently used as a TypedDict since it can be used as a part of a
# Pydantic class but a Pydantic class can not inherit from TypedDict
# and and BaseModel
class RevealedAttribute(TypedDict, total=False):
    sub_proof_index: int
    values: dict


class VCUserinfo(Userinfo):
    """
    User database for VC-based Identity provider: since no users are
    known ahead of time, a new user is created with
    every authentication request.
    """

    def __getitem__(self, item):
        """
        There is no user info database, we always return an empty dictionary
        """
        return {}

    def get_claims_for(self, user_id, requested_claims, userinfo=None):
        # type: (str, Mapping[str, Optional[Mapping[str, Union[str, List[str]]]]) -> Dict[str, Union[str, List[str]]]
        """
        There is no user info database, we always return an empty dictionary
        """
        return {}
