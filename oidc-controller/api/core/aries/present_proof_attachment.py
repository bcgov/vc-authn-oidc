import json
import base64

from typing import Dict
from pydantic import BaseModel, Field


class PresentProofv10Attachment(BaseModel):
    # https://github.com/hyperledger/aries-rfcs/blob/main/features/0037-present-proof/README.md#request-presentation
    id: str = Field(default="libindy-request-presentation-0", alias="@id")
    mime_type: str = Field(default="application/json", alias="mime-type")
    data: Dict

    @classmethod
    def build(
        cls, presentation_request
    ) -> "PresentProofv10Attachment":  # bundle everything needed for the QR code
        return cls(
            data={
                "base64": base64.b64encode(
                    json.dumps(presentation_request).encode("ascii")
                ).decode("ascii")
            }
        )
