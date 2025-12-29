from app.context.user.application.contracts import FindUserHandlerContract
from app.context.user.application.dto import FindUserErrorCode, FindUserResult
from app.context.user.application.queries import FindUserQuery
from app.context.user.domain.contracts.infrastructure import UserRepositoryContract
from app.context.user.domain.exceptions import InvalidEmailFormatError
from app.context.user.domain.value_objects import UserEmail, UserID


class FindUserHandler(FindUserHandlerContract):
    """Handler for find user query"""

    def __init__(self, user_repo: UserRepositoryContract):
        self._user_repo = user_repo

    async def handle(self, query: FindUserQuery) -> FindUserResult:
        """
        Execute the find user query.
        Catches all exceptions and returns Result with error codes.
        """
        try:
            # Convert query primitives to value objects
            email = UserEmail(query.email) if query.email is not None else None
            user_id = UserID(query.user_id) if query.user_id is not None else None

            # Call repository
            user_dto = await self._user_repo.find_user(user_id=user_id, email=email)

            # Check if user was found
            if user_dto is None:
                return FindUserResult(
                    error_code=FindUserErrorCode.USER_NOT_FOUND,
                    error_message="User not found",
                )

            # Return success with primitives
            return FindUserResult(
                user_id=user_dto.user_id.value,
                email=user_dto.email.value,
                password=user_dto.password.value,
                username=user_dto.username.value if user_dto.username else None,
            )

        # Catch specific validation exceptions
        except InvalidEmailFormatError:
            return FindUserResult(
                error_code=FindUserErrorCode.INVALID_EMAIL,
                error_message="Invalid email format",
            )
        except ValueError as e:
            # Catch value object validation errors (UserID, etc.)
            error_message = str(e)
            if "user ID" in error_message.lower():
                return FindUserResult(
                    error_code=FindUserErrorCode.INVALID_USER_ID,
                    error_message="Invalid user ID",
                )
            return FindUserResult(
                error_code=FindUserErrorCode.UNEXPECTED_ERROR,
                error_message="Validation error",
            )

        # Catch-all for unexpected errors
        except Exception:
            return FindUserResult(
                error_code=FindUserErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error occurred",
            )
