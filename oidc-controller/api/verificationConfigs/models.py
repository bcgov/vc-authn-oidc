from sqlmodel import Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON

from api.core.models import BaseSQLModel
from .examples import ex_ver_config_read, ex_ver_config_create, ex_ver_config_patch


prefix = "ver_conf"


class VerificationConfigBase(BaseSQLModel):
    ver_config_id: str = Field(primary_key=True)
    subject_identifier: str = Field()
    proof_request: dict = Field(sa_column=Column(JSON))

    def generate_proof_request(self):
        result = {
            "name": "proof_requested",
            "version": "0.0.1",
            "requested_attributes": {},
            "requested_predicates": {},
        }
        for i, req_attr in enumerate(self.proof_request["requested_attributes"]):
            label = req_attr.get("label") or "req_attr_" + str(i)
            result["requested_attributes"][label] = req_attr
        for req_pred in self.proof_request["requested_predicates"]:
            label = req_pred.get("label") or "req_pred_" + str(i)
            result["requested_predicates"][label] = req_pred
        return result


class VerificationConfig(VerificationConfigBase, table=True):
    __tablename__ = f"{prefix}_ver_configs"


class VerificationConfigRead(VerificationConfigBase):
    class Config:
        schema_extra = {"example": ex_ver_config_read}


class VerificationConfigCreate(VerificationConfigBase):
    class Config:
        schema_extra = {"example": ex_ver_config_create}


class VerificationConfigPatch(VerificationConfigBase):
    # nickname: Optional[str] = sqlm.Field(max_length=255)

    class Config:
        schema_extra = {"example": ex_ver_config_patch}
