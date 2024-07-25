import json
import base64

from typing import Dict
from pydantic import BaseModel, Field


class PresentProofv20Attachment(BaseModel):
    # https://github.com/hyperledger/aries-rfcs/tree/eace815c3e8598d4a8dd7881d8c731fdb2bcc0aa/features/0454-present-proof-v2
    id: str = Field(default="libindy-request-presentation-0", alias="@id")
    mime_type: str = Field(default="application/json", alias="mime-type")
    data: Dict

    @classmethod
    def build(
        cls, presentation_request
    ) -> "PresentProofv20Attachment":  # bundle everything needed for the QR code
        return cls(
            data={
                "base64": base64.b64encode(
                    json.dumps(presentation_request).encode("ascii")
                ).decode("ascii")
            }
        )
