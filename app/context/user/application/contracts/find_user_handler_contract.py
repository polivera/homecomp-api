from abc import ABC, abstractmethod

from app.context.user.application.dto import FindUserResult
from app.context.user.application.queries import FindUserQuery


class FindUserHandlerContract(ABC):
    """Contract for FindUser query handler"""

    @abstractmethod
    async def handle(self, query: FindUserQuery) -> FindUserResult:
        """
        Handle find user query.

        Args:
            query: FindUserQuery with user_id and/or email

        Returns:
            FindUserResult with user data or error information
        """
        pass
