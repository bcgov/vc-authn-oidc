from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from api.core.config import settings

from .examples import ex_client_config_create


class TOKENENDPOINTAUTHMETHODS(str, Enum):
    client_secret_basic = "client_secret_basic"


class ClientConfigurationBase(BaseModel):
    client_id: str = Field(default=settings.KEYCLOAK_CLIENT_ID)
    client_name: str = Field(default=settings.KEYCLOAK_CLIENT_NAME)
    response_types: List[str] = Field(default=["code", "id_token", "token"])
    redirect_uris: List[str]
    token_endpoint_auth_method: TOKENENDPOINTAUTHMETHODS = Field(
        default=TOKENENDPOINTAUTHMETHODS.client_secret_basic
    )

    client_secret: str = Field(default=settings.KEYCLOAK_CLIENT_SECRET)

    class Config:
        allow_population_by_field_name = True


class ClientConfiguration(ClientConfigurationBase):
    pass


class ClientConfigurationRead(ClientConfigurationBase):
    pass


class ClientConfigurationCreate(ClientConfigurationBase):
    class Config:
        schema_extra = {"example": ex_client_config_create}


class ClientConfigurationPatch(ClientConfigurationBase):
    client_id: Optional[str]
    client_name: Optional[str]
    response_types: Optional[List[str]]
    redirect_uris: Optional[List[str]]
    token_endpoint_auth_method: Optional[TOKENENDPOINTAUTHMETHODS]

    client_secret: Optional[str]
