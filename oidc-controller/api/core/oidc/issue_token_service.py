import logging
from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel

from ...authSessions.models import AuthSession
from ...verificationConfigs.models import VerificationConfig

logger = logging.getLogger(__name__)


class Claim(BaseModel):
    type: str
    value: str


class Token(BaseModel):
    creation_time: datetime = datetime.now()
    issuer: str
    audiences: List[str]
    lifetime: int
    claims: Dict[str, Claim]

    @classmethod
    def get_claims(
        cls, pres_exch: Dict, auth_session: AuthSession, ver_config: VerificationConfig
    ) -> List["Claim"]:
        """Converts vc presentation values to oidc claims"""
        logger.debug(f">>> Token.get_claims")
        logger.info(pres_exch)

        claims: List[Claim] = [
            Claim(
                type="pres_req_conf_id",
                value=auth_session.request_parameters["pres_req_conf_id"],
            ),
            Claim(type="acr", value="vc_authn"),
        ]

        # subject claim
        logger.info(ver_config.subject_identifier)
        claims.append(
            Claim(type="sub", value="FROM_PROOF_REQUEST")
        )  # TODO, get this from presentation
        claims.append(
            Claim(type="nonce", value=auth_session.request_parameters["nonce"])
        )

        for requested_attr in auth_session.presentation_exchange[
            "presentation_request"
        ]["requested_attributes"].values():
            # loop through each value and put it in token as a claim
            revealed_attrs: Dict = auth_session.presentation_exchange["presentation"][
                "requested_proof"
            ]["revealed_attrs"]
            for k, v in revealed_attrs.items():
                claims.append(Claim(type=requested_attr["name"], value=v["raw"]))
            return {c.type: c for c in claims}

    # renames and calculates dict members appropriate to https://openid.net/specs/openid-connect-core-1_0.html#IDToken
    # and
    # https://github.com/OpenIDC/pyoidc/blob/26ea5121239dad03c5c5551cca149cb984df1ec9/src/oic/oic/message.py#L720

    def idtoken_dict(self, nonce: str) -> Dict:
        """Converts oidc claims to IdToken attribute names"""

        result = {}  # nest VC attribute claims under the key=pres_req_conf_id
        for claim in self.claims.values():
            result[claim.type] = claim.value

        result[
            "sub"
        ] = "1af58203-33fa-42a6-8628-a85472a9967e"  # TODO make this dependant on ver_config
        result["t_id"] = "132465e4-c57f-459f-8534-e30e78484f24"  # what this do?
        result["exp"] = int(round(datetime.now().timestamp())) + self.lifetime
        result["aud"] = self.audiences
        result["nonce"] = nonce

        return result
