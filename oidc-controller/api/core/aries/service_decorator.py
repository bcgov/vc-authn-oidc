from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ServiceDecorator(BaseModel):
    # https://github.com/hyperledger/aries-rfcs/tree/main/features/0056-service-decorator
    recipient_keys: Optional[List[str]] = Field(default=None, alias="recipientKeys")
    routing_keys: Optional[List[str]] = Field(default=None, alias="routingKeys")
    service_endpoint: Optional[str] = Field(default=None, alias="serviceEndpoint")

    model_config = ConfigDict(populate_by_name=True)


class OOBServiceDecorator(ServiceDecorator):
    # ServiceDecorator
    recipient_keys: Optional[List[str]] = None
    routing_keys: Optional[List[str]] = Field(default=[])
    service_endpoint: Optional[str] = None
    id: str = Field(default="did:vc-authn-oidc:123456789zyxwvutsr#did-communication")
    type: str = Field(default="did-communication")
    priority: int = 0

    model_config = ConfigDict(populate_by_name=True)
