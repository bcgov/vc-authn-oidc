from typing import List, Optional
from pydantic import BaseModel, Field


class ServiceDecorator(BaseModel):
    # https://github.com/hyperledger/aries-rfcs/tree/main/features/0056-service-decorator
    recipient_keys: Optional[List[str]] = Field(alias="recipientKeys")
    routing_keys: Optional[List[str]] = Field(alias="routingKeys")
    service_endpoint: Optional[str] = Field(alias="serviceEndpoint")

    class Config:
        allow_population_by_field_name = True
