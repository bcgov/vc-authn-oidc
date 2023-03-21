from enum import Enum
from typing import List
from pydantic import BaseModel, Field

from api.core.models import UUIDModel
from api.core.config import settings


class TOKENENDPOINTAUTHMETHODS(str, Enum):
    client_secret_basic = "client_secret_basic"


class ClientConfigurationBase(BaseModel):
    client_id: str = Field(default=settings.KEYCLOAK_CLIENT_ID)
    client_name: str = Field(default=settings.KEYCLOAK_CLIENT_NAME)
    response_types: List[str] = Field(default=["code", "id_token", "token"])
    redirect_uris: List[str] = Field(default=[settings.KEYCLOAK_REDIRECT_URI])
    token_endpoint_auth_method: TOKENENDPOINTAUTHMETHODS = Field(
        default=TOKENENDPOINTAUTHMETHODS.client_secret_basic
    )

    client_secret: str = Field(default=settings.KEYCLOAK_CLIENT_SECRET)

    class Config:
        allow_population_by_field_name = True


class ClientConfiguration(ClientConfigurationBase, UUIDModel):
    pass


class ClientConfigurationCreate(ClientConfigurationBase):
    pass


class ClientConfigurationPatch(ClientConfigurationBase):
    pass
