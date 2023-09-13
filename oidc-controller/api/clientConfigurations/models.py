from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from .examples import ex_client_config
from ..core.config import settings


class TOKENENDPOINTAUTHMETHODS(str, Enum):
    client_secret_basic = "client_secret_basic"


class ClientConfigurationBase(BaseModel):
    client_id: str = Field(default=settings.OIDC_CLIENT_ID)
    client_name: str = Field(default=settings.OIDC_CLIENT_NAME)
    response_types: List[str] = Field(default=["code", "id_token", "token"])
    redirect_uris: List[str]
    token_endpoint_auth_method: TOKENENDPOINTAUTHMETHODS = Field(
        default=TOKENENDPOINTAUTHMETHODS.client_secret_basic
    )

    client_secret: str = Field(default=settings.OIDC_CLIENT_SECRET)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {"example": ex_client_config}


class ClientConfiguration(ClientConfigurationBase):
    pass


class ClientConfigurationRead(ClientConfigurationBase):
    pass


class ClientConfigurationPatch(ClientConfigurationBase):
    client_id: Optional[str]
    client_name: Optional[str]
    response_types: Optional[List[str]]
    redirect_uris: Optional[List[str]]
    token_endpoint_auth_method: Optional[TOKENENDPOINTAUTHMETHODS]
    client_secret: Optional[str]

    pass
