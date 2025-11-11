import abc
from uuid import UUID

class CoreApiClient(abc.ABC):

    @abc.abstractmethod
    def get_user_core_info(self, user_id: UUID) -> dict:
        """
        Get the core information of a user.

        Args:
            user_id: The id of the user.

        Returns:
            The core information of the user.
        """
        pass

    @abc.abstractmethod
    def verify_subscription(self, subscription_id: UUID, metadata: dict) -> dict:
        """
        Verify the subscription of a user.

        Args:
            subscription_id: The id of the subscription.
            metadata: The metadata of the subscription.
        Returns:
            The result of the verification.
        """
        pass