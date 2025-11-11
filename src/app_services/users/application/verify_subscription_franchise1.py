from typing import Optional
from uuid import UUID
from app_services.users.application import VerifySubscriptionInterface
from app_services.users.domain import CoreApiClient

class VerifySubscriptionFranchise1(VerifySubscriptionInterface):

    def __init__(self, core_api_client: CoreApiClient):
        self.core_api_client = core_api_client

    def verify(
        self, 
        metadata: dict, 
        subscription_id: Optional[UUID], 
        subscription_external_id: Optional[str]
    ) -> dict:
        
        result = self.core_api_client.verify_subscription(subscription_id, metadata)
        return result
        