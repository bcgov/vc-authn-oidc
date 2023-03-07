from typing import List, Optional
from pydantic import BaseModel, Field


class ServiceDecorator(BaseModel):
    # https://github.com/hyperledger/aries-rfcs/tree/main/features/0056-service-decorator
    recipient_keys: Optional[List[str]] = Field(alias="recipientKeys")
    routing_keys: Optional[List[str]] = Field(alias="routingKeys")
    service_endpoint: Optional[str] = Field(alias="serviceEndpoint")

    class Config:
        allow_population_by_field_name = True


class OOBServiceDecorator(ServiceDecorator):
    # ServiceDecorator
    recipient_keys: Optional[List[str]]
    routing_keys: Optional[List[str]] = Field(default=[])
    service_endpoint: Optional[str]
    id: str = Field(default="did:vc-authn-oidc:123456789zyxwvutsr#did-communication")
    type: str = Field(default="did-communication")
    priority: int = 0

    class Config:
        allow_population_by_field_name = True
