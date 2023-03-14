import time
from typing import Optional, List
from pydantic import BaseModel, Field

from .examples import ex_ver_config_read, ex_ver_config_create
from ..core.config import settings


# Slightly modified from ACAPY models.
class AttributeFilter(BaseModel):
    schema_id: Optional[str]
    cred_def_id: Optional[str]
    schema_name: Optional[str]
    schema_issuer_did: Optional[str]
    schema_version: Optional[str]
    issuer_did: Optional[str]


class ReqAttr(BaseModel):
    name: str
    names: Optional[List[str]]
    label: Optional[str]
    restrictions: List[AttributeFilter]


class ReqPred(BaseModel):
    name: str
    label: Optional[str]
    restrictions: List[AttributeFilter]
    p_value: str
    p_type: str


class VerificationProofRequest(BaseModel):
    name: Optional[str]
    version: str = Field(regex="[0-9](.[0.9])*", example="0.0.1")
    non_revoked: Optional[str]
    requested_attributes: List[ReqAttr]
    requested_predicates: List[ReqPred]


class VerificationConfigBase(BaseModel):
    ver_config_id: str = Field()
    subject_identifier: str = Field()
    proof_request: VerificationProofRequest = Field()

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
        for req_pred in self.proof_request.requested_predicates:
            label = req_pred.label or "req_pred_" + str(i)
            result["requested_predicates"][label] = req_pred.dict(exclude_none=True)
            if settings.SET_NON_REVOKED:
                result["requested_attributes"][label]["non_revoked"] = {
                    "from": int(time.time()),
                    "to": int(time.time()),
                }
        return result

    class Config:
        schema_extra = {"example": ex_ver_config_create}


class VerificationConfig(VerificationConfigBase):
    pass


class VerificationConfigRead(VerificationConfigBase):
    class Config:
        schema_extra = {"example": ex_ver_config_read}


class VerificationConfigCreate(VerificationConfigBase):
    class Config:
        schema_extra = {"example": ex_ver_config_create}


class VerificationConfigPatch(VerificationConfigBase):
    pass
