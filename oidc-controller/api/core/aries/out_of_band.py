from typing import Dict, List
from pydantic import BaseModel, Field


class OutOfBandPresentProofAttachment(BaseModel):
    id: str = Field(alias="@id")
    mime_type: str = Field(default="application/json", alias="mime-type")
    data: Dict

    class Config:
        allow_population_by_field_name = True


class OutOfBandMessage(BaseModel):
    # https://github.com/hyperledger/aries-rfcs/blob/main/features/0434-outofband
    id: str = Field(alias="@id")
    type: str = Field(
        default="https://didcomm.org/out-of-band/1.1/invitation",
        alias="@type",
    )
    goal_code: str = Field(default="request-proof")
    label: str = Field(
        default="vc-authn Out-of-Band present-proof authorization request"
    )
    request_attachments: List[OutOfBandPresentProofAttachment] = Field(
        alias="requests~attach"
    )
    services: List[str] = Field(alias="services")

    class Config:
        allow_population_by_field_name = True
