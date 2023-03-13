import json
import base64
from typing import Optional, List

from pydantic import BaseModel, Field
from api.core.aries import PresentProofv10Attachment, ServiceDecorator


class PresentationRequestMessage(BaseModel):
    # https://github.com/hyperledger/aries-rfcs/blob/main/features/0037-present-proof/README.md#presentation
    id: str = Field(alias="@id")
    type: str = Field(
        "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation",
        alias="@type",
    )
    request: List[PresentProofv10Attachment] = Field(
        alias="request_presentations~attach"
    )
    comment: str = None
    service: Optional[ServiceDecorator] = Field(alias="~service")

    class Config:
        allow_population_by_field_name = True

    def b64_str(self):
        # object->dict->jsonString->ascii->ENCODE->ascii
        return base64.b64encode(
            json.dumps(self.dict(by_alias=True)).encode("ascii")
        ).decode("ascii")
