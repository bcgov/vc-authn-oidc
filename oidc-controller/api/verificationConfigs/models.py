import time
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

from .examples import ex_ver_config
from ..core.config import settings


# Slightly modified from ACAPY models.
class AttributeFilter(BaseModel):
    schema_id: Optional[str] = None
    cred_def_id: Optional[str] = None
    schema_name: Optional[str] = None
    schema_issuer_did: Optional[str] = None
    schema_version: Optional[str] = None
    issuer_did: Optional[str] = None


class ReqAttr(BaseModel):
    names: List[str]
    label: Optional[str] = None
    restrictions: List[AttributeFilter]


class ReqPred(BaseModel):
    name: str
    label: Optional[str] = None
    restrictions: List[AttributeFilter]
    p_value: str
    p_type: str


class VerificationProofRequest(BaseModel):
    name: Optional[str] = None
    version: str = Field(pattern="[0-9](.[0.9])*", example="0.0.1")
    non_revoked: Optional[str] = None
    requested_attributes: List[ReqAttr]
    requested_predicates: List[ReqPred]


class VerificationConfigBase(BaseModel):
    subject_identifier: str = Field()
    proof_request: VerificationProofRequest = Field()
    generate_consistent_identifier: Optional[bool] = Field(default=False)
    include_v1_attributes: Optional[bool] = Field(default=False)

    def generate_proof_request(self):
        result = {
            "name": "proof_requested",
            "version": "0.0.1",
            "requested_attributes": {},
            "requested_predicates": {},
        }
        for i, req_attr in enumerate(self.proof_request.requested_attributes):
            label = req_attr.label or "req_attr_" + str(i)
            result["requested_attributes"][label] = req_attr.dict(exclude_none=True)
            if settings.SET_NON_REVOKED:
                result["requested_attributes"][label]["non_revoked"] = {
                    "from": int(time.time()),
                    "to": int(time.time()),
                }
        # TODO add I indexing
        for req_pred in self.proof_request.requested_predicates:
            label = req_pred.label or "req_pred_" + str(i)
            result["requested_predicates"][label] = req_pred.dict(exclude_none=True)
            if settings.SET_NON_REVOKED:
                result["requested_attributes"][label]["non_revoked"] = {
                    "from": int(time.time()),
                    "to": int(time.time()),
                }
        return result
    
    model_config = ConfigDict(schema_extra={"example": ex_ver_config})


class VerificationConfig(VerificationConfigBase):
    ver_config_id: str = Field()


class VerificationConfigRead(VerificationConfigBase):
    ver_config_id: str = Field()


class VerificationConfigPatch(VerificationConfigBase):
    subject_identifier: Optional[str] = Field()
    proof_request: Optional[VerificationProofRequest] = Field()

    pass
