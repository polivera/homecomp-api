from datetime import datetime, timedelta

import pytest

from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.dto import (
    LoginHandlerResultDTO,
    LoginHandlerResultStatus,
)
from app.context.auth.application.handlers.login_handler import LoginHandler
from app.context.auth.domain.exceptions import (
    AccountBlockedException,
    InvalidCredentialsException,
)
from app.context.auth.domain.value_objects import SessionToken
from app.context.user.application.dto import FindUserResult


@pytest.mark.unit
@pytest.mark.asyncio
class TestLoginHandler:
    """Unit tests for LoginHandler."""

    async def test_handle_successful_login(self, mock_find_user_handler, mock_login_service, mock_logger):
        """Test successful login returns token and user_id."""
        # Arrange
        email = "test@example.com"
        password = "password123"
        user_id = 42
        hashed_password = "$argon2id$v=19$m=65536,t=3,p=4$somehash"
        token_value = "secure-session-token-xyz"

        mock_user = FindUserResult(user_id=user_id, email=email, password=hashed_password)
        mock_find_user_handler.handle_mock.return_value = mock_user
        mock_login_service.handle_mock.return_value = SessionToken(token_value)

        handler = LoginHandler(mock_find_user_handler, mock_login_service, mock_logger)
        command = LoginCommand(email=email, password=password)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is not None
        assert isinstance(result, LoginHandlerResultDTO)
        assert result.status == LoginHandlerResultStatus.SUCCESS
        assert result.token == token_value
        assert result.user_id == user_id
        assert result.error_msg is None
        assert result.retry_after is None

        # Verify find user handler was called correctly
        mock_find_user_handler.handle_mock.assert_called_once()
        call_args = mock_find_user_handler.handle_mock.call_args[0][0]
        assert call_args.email == email

        # Verify login service was called with correct parameters
        mock_login_service.handle_mock.assert_called_once()

    async def test_handle_user_not_found(self, mock_find_user_handler, mock_login_service, mock_logger):
        """Test that login fails when user is not found."""
        # Arrange
        email = "nonexistent@example.com"
        password = "password123"

        mock_find_user_handler.handle_mock.return_value = None

        handler = LoginHandler(mock_find_user_handler, mock_login_service, mock_logger)
        command = LoginCommand(email=email, password=password)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is not None
        assert result.status == LoginHandlerResultStatus.INVALID_CREDENTIALS
        assert result.error_msg == "Invalid username or password"
        assert result.token is None
        assert result.user_id is None
        assert result.retry_after is None

        # Verify login service was NOT called since user not found
        mock_login_service.handle_mock.assert_not_called()

    async def test_handle_invalid_credentials_exception(self, mock_find_user_handler, mock_login_service, mock_logger):
        """Test that InvalidCredentialsException is handled correctly."""
        # Arrange
        email = "test@example.com"
        password = "wrongpassword"
        user_id = 10
        hashed_password = "$argon2id$v=19$m=65536,t=3,p=4$somehash"

        mock_user = FindUserResult(user_id=user_id, email=email, password=hashed_password)
        mock_find_user_handler.handle_mock.return_value = mock_user
        mock_login_service.handle_mock.side_effect = InvalidCredentialsException()

        handler = LoginHandler(mock_find_user_handler, mock_login_service, mock_logger)
        command = LoginCommand(email=email, password=password)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is not None
        assert result.status == LoginHandlerResultStatus.INVALID_CREDENTIALS
        assert result.error_msg == "Invalid username or password"
        assert result.token is None
        assert result.user_id is None
        assert result.retry_after is None

        # Verify login service was called
        mock_login_service.handle_mock.assert_called_once()

    async def test_handle_account_blocked_exception(self, mock_find_user_handler, mock_login_service, mock_logger):
        """Test that AccountBlockedException is handled correctly."""
        # Arrange
        email = "blocked@example.com"
        password = "password123"
        user_id = 99
        hashed_password = "$argon2id$v=19$m=65536,t=3,p=4$somehash"
        blocked_until = datetime.now() + timedelta(minutes=15)

        mock_user = FindUserResult(user_id=user_id, email=email, password=hashed_password)
        mock_find_user_handler.handle_mock.return_value = mock_user
        mock_login_service.handle_mock.side_effect = AccountBlockedException(blocked_until)

        handler = LoginHandler(mock_find_user_handler, mock_login_service, mock_logger)
        command = LoginCommand(email=email, password=password)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is not None
        assert result.status == LoginHandlerResultStatus.ACCOUNT_BLOCKED
        assert result.error_msg == "Account is blocked, try again later"
        assert result.retry_after == blocked_until
        assert result.token is None
        assert result.user_id is None

        # Verify login service was called
        mock_login_service.handle_mock.assert_called_once()

    async def test_handle_unexpected_error(self, mock_find_user_handler, mock_login_service, mock_logger):
        """Test that unexpected exceptions are handled gracefully."""
        # Arrange
        email = "error@example.com"
        password = "password123"
        user_id = 50
        hashed_password = "$argon2id$v=19$m=65536,t=3,p=4$somehash"

        mock_user = FindUserResult(user_id=user_id, email=email, password=hashed_password)
        mock_find_user_handler.handle_mock.return_value = mock_user
        mock_login_service.handle_mock.side_effect = RuntimeError("Unexpected error")

        handler = LoginHandler(mock_find_user_handler, mock_login_service, mock_logger)
        command = LoginCommand(email=email, password=password)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is not None
        assert result.status == LoginHandlerResultStatus.UNEXPECTED_ERROR
        assert result.error_msg == "Unexpected error"
        assert result.token is None
        assert result.user_id is None
        assert result.retry_after is None

        # Verify login service was called
        mock_login_service.handle_mock.assert_called_once()

    async def test_handle_database_exception(self, mock_find_user_handler, mock_login_service, mock_logger):
        """Test that database-related exceptions are handled as unexpected errors."""
        # Arrange
        email = "db-error@example.com"
        password = "password123"
        user_id = 25
        hashed_password = "$argon2id$v=19$m=65536,t=3,p=4$somehash"

        mock_user = FindUserResult(user_id=user_id, email=email, password=hashed_password)
        mock_find_user_handler.handle_mock.return_value = mock_user
        mock_login_service.handle_mock.side_effect = Exception("Database connection lost")

        handler = LoginHandler(mock_find_user_handler, mock_login_service, mock_logger)
        command = LoginCommand(email=email, password=password)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result is not None
        assert result.status == LoginHandlerResultStatus.UNEXPECTED_ERROR
        assert result.error_msg == "Unexpected error"

    async def test_handle_passes_correct_auth_user_dto(self, mock_find_user_handler, mock_login_service, mock_logger):
        """Test that handler correctly constructs AuthUserDTO from UserContextDTO."""
        # Arrange
        email = "dto-test@example.com"
        password = "password123"
        user_id = 777
        hashed_password = "$argon2id$v=19$m=65536,t=3,p=4$correcthash"

        mock_user = FindUserResult(user_id=user_id, email=email, password=hashed_password)
        mock_find_user_handler.handle_mock.return_value = mock_user
        mock_login_service.handle_mock.return_value = SessionToken("test-token")

        handler = LoginHandler(mock_find_user_handler, mock_login_service, mock_logger)
        command = LoginCommand(email=email, password=password)

        # Act
        await handler.handle(command)

        # Assert - verify login service received correctly constructed AuthUserDTO
        mock_login_service.handle_mock.assert_called_once()
        call_kwargs = mock_login_service.handle_mock.call_args.kwargs

        # Verify user_password
        assert call_kwargs["user_password"].value == password

        # Verify db_user structure
        db_user = call_kwargs["db_user"]
        assert db_user.user_id.value == user_id
        assert db_user.email.value == email
        assert db_user.password.value == hashed_password

    async def test_handle_with_different_user_scenarios(self, mock_find_user_handler, mock_login_service, mock_logger):
        """Test login with various user scenarios."""
        # Arrange
        test_cases = [
            {
                "email": "admin@example.com",
                "user_id": 1,
                "description": "admin user",
            },
            {
                "email": "user@domain.co.uk",
                "user_id": 9999,
                "description": "high user id",
            },
            {
                "email": "test+tag@example.com",
                "user_id": 123,
                "description": "email with plus addressing",
            },
        ]

        for test_case in test_cases:
            # Reset mocks for each test case
            mock_find_user_handler.handle_mock.reset_mock()
            mock_login_service.handle_mock.reset_mock()

            email = test_case["email"]
            user_id = test_case["user_id"]
            password = "testpassword"
            hashed_password = "$argon2id$v=19$m=65536,t=3,p=4$hash"

            mock_user = FindUserResult(user_id=user_id, email=email, password=hashed_password)
            mock_find_user_handler.handle_mock.return_value = mock_user
            mock_login_service.handle_mock.return_value = SessionToken(f"token-{user_id}")

            handler = LoginHandler(mock_find_user_handler, mock_login_service, mock_logger)
            command = LoginCommand(email=email, password=password)

            # Act
            result = await handler.handle(command)

            # Assert
            assert result.status == LoginHandlerResultStatus.SUCCESS
            assert result.user_id == user_id
            assert result.token == f"token-{user_id}"
