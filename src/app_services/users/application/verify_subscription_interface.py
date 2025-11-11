import abc
from typing import Optional
from uuid import UUID

class VerifySubscriptionInterface(abc.ABC):

    @abc.abstractmethod
    def verify(
        self, 
        metadata: dict, 
        subscription_id: Optional[UUID], 
        subscription_external_id: Optional[str]
    ) -> dict:
        """
        Verify the subscription of a user.

        Args:
            metadata: The metadata of the subscription.
            subscription_id: The id of the subscription.
            subscription_external_id: The external id of the subscription.

        Returns:
            The result of the verification.
        """
        pass