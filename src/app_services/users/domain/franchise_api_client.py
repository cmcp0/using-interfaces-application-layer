import abc

class FranchiseApiClient(abc.ABC):

    @abc.abstractmethod
    def get_user_subscription_info(self, subscription_external_id: str) -> dict:
        """
        Get the information of a user's subscription.

        Args:
            subscription_external_id: The external id of the subscription.

        Returns:
            The information of the user's subscription.
        """
        pass