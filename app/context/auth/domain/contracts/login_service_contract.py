from abc import ABC, abstractmethod

from app.context.auth.domain.dto import AuthUserDTO
from app.context.auth.domain.value_objects import AuthPassword, SessionToken


class LoginServiceContract(ABC):
    @abstractmethod
    async def handle(
        self, user_password: AuthPassword, db_user: AuthUserDTO
    ) -> SessionToken:
        """
        Handle user login.

        Args:
            user_password: The plaintext password to verify
            db_user: The user attempting to login

        Returns:
            SessionToken: A new session token on successful login

        Raises:
            InvalidCredentialsException: If password is incorrect
            AccountBlockedException: If account is temporarily blocked
        """
        pass
