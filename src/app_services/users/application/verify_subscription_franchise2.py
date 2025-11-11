from typing import Optional
from uuid import UUID
from app_services.users.application import VerifySubscriptionInterface
from app_services.users.domain import CoreApiClient, FranchiseApiClient

class VerifySubscriptionFranchise2(VerifySubscriptionInterface):

    def __init__(
        self, 
        core_api_client: CoreApiClient, 
        franchise_api_client: FranchiseApiClient
    ):
        self.franchise_api_client = franchise_api_client
        self.core_api_client = core_api_client

    def verify(
        self, 
        metadata: dict, 
        subscription_id: Optional[UUID], 
        subscription_external_id: Optional[str]
    ) -> dict:
        user_subscription_info = self.franchise_api_client.get_user_subscription_info(
            subscription_external_id
        )
        if user_subscription_info is None:
            return {
                "status": "error",
                "message": "User subscription not found",
            }
        if user_subscription_info["status"] != "active":
            return {
                "status": "error",
                "message": "User subscription is not active",
            }
        subscription_id = user_subscription_info["id"]
        if subscription_id is None:
            return {
                "status": "error",
                "message": "Subscription id not found",
            }
            
        return self.core_api_client.verify_subscription(subscription_id, metadata)
