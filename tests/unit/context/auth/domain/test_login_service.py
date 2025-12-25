"""Unit tests for LoginService."""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest

from app.context.auth.domain.dto import AuthUserDTO, SessionDTO
from app.context.auth.domain.exceptions import (
    AccountBlockedException,
    InvalidCredentialsException,
)
from app.context.auth.domain.services.login_service import LoginService
from app.context.auth.domain.value_objects import (
    AuthEmail,
    AuthPassword,
    AuthUserID,
    FailedLoginAttempts,
    SessionToken,
)
from app.context.auth.domain.value_objects.blocked_time import BlockedTime


@pytest.mark.unit
@pytest.mark.asyncio
class TestLoginService:
    """Unit tests for LoginService domain service."""

    async def test_successful_login_no_existing_session(self, mock_session_repository):
        """Test successful login when no session exists - creates new session."""
        # Arrange
        user_id = AuthUserID(42)
        plain_password = "correct_password"
        hashed_password = AuthPassword.from_plain_text(plain_password)
        user_password = AuthPassword.keep_plain(plain_password)

        db_user = AuthUserDTO(
            user_id=user_id,
            email=AuthEmail("test@example.com"),
            password=hashed_password,
        )

        # Mock repository to return None (no session exists)
        mock_session_repository.get_session_mock.return_value = None

        # Mock createSession to return new session
        new_session = SessionDTO(
            user_id=user_id,
            token=None,
            failed_attempts=FailedLoginAttempts(0),
            blocked_until=None,
        )
        mock_session_repository.create_session_mock.return_value = new_session

        # Mock updateSession to return updated session
        mock_session_repository.update_session_mock.return_value = SessionDTO(
            user_id=user_id,
            token=SessionToken("mocked-token"),
            failed_attempts=FailedLoginAttempts(0),
            blocked_until=None,
        )

        service = LoginService(mock_session_repository)

        # Act
        with patch.object(
            SessionToken, "generate", return_value=SessionToken("mocked-token")
        ):
            result = await service.handle(user_password, db_user)

        # Assert
        assert isinstance(result, SessionToken)
        assert result.value == "mocked-token"

        # Verify getSession was called
        # mock_session_repository.get_session_mock.assert_called_once()
        mock_session_repository.get_session_mock.assert_called_once_with(
            user_id=user_id, token=None
        )

        # Verify createSession was called
        mock_session_repository.create_session_mock.assert_called_once()
        created_session = mock_session_repository.create_session_mock.call_args[0][0]
        assert created_session.user_id == user_id
        assert created_session.token is None
        assert created_session.failed_attempts.value == 0
        assert created_session.blocked_until is None

        # Verify updateSession was called with token and reset attempts
        mock_session_repository.update_session_mock.assert_called_once()
        updated_session = mock_session_repository.update_session_mock.call_args[0][0]
        assert updated_session.user_id == user_id
        assert updated_session.token.value == "mocked-token"
        assert updated_session.failed_attempts.value == 0
        assert updated_session.blocked_until is None

    async def test_successful_login_with_existing_session(
        self, mock_session_repository
    ):
        """Test successful login when session already exists."""
        # Arrange
        user_id = AuthUserID(99)
        plain_password = "secure_password"
        hashed_password = AuthPassword.from_plain_text(plain_password)
        user_password = AuthPassword.keep_plain(plain_password)

        db_user = AuthUserDTO(
            user_id=user_id,
            email=AuthEmail("existing@example.com"),
            password=hashed_password,
        )

        # Mock existing session
        existing_session = SessionDTO(
            user_id=user_id,
            token=SessionToken("old-token"),
            failed_attempts=FailedLoginAttempts(0),
            blocked_until=None,
        )
        mock_session_repository.get_session_mock.return_value = existing_session

        service = LoginService(mock_session_repository)

        # Act
        with patch.object(
            SessionToken, "generate", return_value=SessionToken("new-token")
        ):
            result = await service.handle(user_password, db_user)

        # Assert
        assert isinstance(result, SessionToken)
        assert result.value == "new-token"

        # Verify createSession was NOT called
        mock_session_repository.create_session_mock.assert_not_called()

        # Verify updateSession was called
        mock_session_repository.update_session_mock.assert_called_once()

    async def test_failed_login_wrong_password_first_attempt(
        self, mock_session_repository
    ):
        """Test failed login increments attempt counter on first wrong password."""
        # Arrange
        user_id = AuthUserID(10)
        correct_password = "correct_password"
        wrong_password = "wrong_password"
        hashed_password = AuthPassword.from_plain_text(correct_password)
        user_password = AuthPassword.keep_plain(wrong_password)

        db_user = AuthUserDTO(
            user_id=user_id,
            email=AuthEmail("user@example.com"),
            password=hashed_password,
        )

        # Mock existing session with 0 failed attempts
        existing_session = SessionDTO(
            user_id=user_id,
            token=None,
            failed_attempts=FailedLoginAttempts(0),
            blocked_until=None,
        )
        mock_session_repository.get_session_mock.return_value = existing_session

        service = LoginService(mock_session_repository)

        # Act & Assert
        with pytest.raises(InvalidCredentialsException):
            with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
                await service.handle(user_password, db_user)

                # Verify sleep was called with correct delay (0 for first attempt)
                mock_sleep.assert_called_once_with(0)

        # Verify updateSession was called with incremented attempts
        mock_session_repository.update_session_mock.assert_called_once()
        updated_session = mock_session_repository.update_session_mock.call_args[0][0]
        assert updated_session.failed_attempts.value == 1
        assert updated_session.blocked_until is None
        assert updated_session.token is None

    async def test_failed_login_third_attempt_with_delay(self, mock_session_repository):
        """Test failed login on third attempt has correct delay."""
        # Arrange
        user_id = AuthUserID(15)
        correct_password = "correct_password"
        wrong_password = "wrong_password"
        hashed_password = AuthPassword.from_plain_text(correct_password)
        user_password = AuthPassword.keep_plain(wrong_password)

        db_user = AuthUserDTO(
            user_id=user_id,
            email=AuthEmail("delayed@example.com"),
            password=hashed_password,
        )

        # Mock session with 2 failed attempts (next will be 3rd)
        existing_session = SessionDTO(
            user_id=user_id,
            token=None,
            failed_attempts=FailedLoginAttempts(2),
            blocked_until=None,
        )
        mock_session_repository.get_session_mock.return_value = existing_session

        service = LoginService(mock_session_repository)

        # Act & Assert
        with pytest.raises(InvalidCredentialsException):
            with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
                await service.handle(user_password, db_user)

                # Verify sleep was called with 2 seconds (3rd attempt delay)
                mock_sleep.assert_called_once_with(2)

        # Verify attempts incremented to 3
        updated_session = mock_session_repository.update_session_mock.call_args[0][0]
        assert updated_session.failed_attempts.value == 3

    async def test_failed_login_max_attempts_blocks_account(
        self, mock_session_repository
    ):
        """Test that reaching max attempts blocks the account."""
        # Arrange
        user_id = AuthUserID(20)
        correct_password = "correct_password"
        wrong_password = "wrong_password"
        hashed_password = AuthPassword.from_plain_text(correct_password)
        user_password = AuthPassword.keep_plain(wrong_password)

        db_user = AuthUserDTO(
            user_id=user_id,
            email=AuthEmail("blocked@example.com"),
            password=hashed_password,
        )

        # Mock session with 3 failed attempts (next will be 4th = max)
        existing_session = SessionDTO(
            user_id=user_id,
            token=None,
            failed_attempts=FailedLoginAttempts(3),
            blocked_until=None,
        )
        mock_session_repository.get_session_mock.return_value = existing_session

        service = LoginService(mock_session_repository)

        # Act & Assert
        with pytest.raises(InvalidCredentialsException):
            with patch("asyncio.sleep", new_callable=AsyncMock):
                await service.handle(user_password, db_user)

        # Verify updateSession was called with blocked_until set
        updated_session = mock_session_repository.update_session_mock.call_args[0][0]
        assert updated_session.failed_attempts.value == 4
        assert updated_session.blocked_until is not None
        assert isinstance(updated_session.blocked_until, BlockedTime)
        # Verify blocked time is in the future
        assert updated_session.blocked_until.value > datetime.now()

    async def test_login_blocked_account_raises_exception(
        self, mock_session_repository
    ):
        """Test that login attempt on blocked account raises AccountBlockedException."""
        # Arrange
        user_id = AuthUserID(25)
        plain_password = "any_password"
        hashed_password = AuthPassword.from_plain_text(plain_password)
        user_password = AuthPassword.keep_plain(plain_password)

        db_user = AuthUserDTO(
            user_id=user_id,
            email=AuthEmail("blocked@example.com"),
            password=hashed_password,
        )

        # Mock session with active block
        blocked_until = datetime.now() + timedelta(minutes=10)
        existing_session = SessionDTO(
            user_id=user_id,
            token=None,
            failed_attempts=FailedLoginAttempts(4),
            blocked_until=BlockedTime(blocked_until),
        )
        mock_session_repository.get_session_mock.return_value = existing_session

        service = LoginService(mock_session_repository)

        # Act & Assert
        with pytest.raises(AccountBlockedException) as exc_info:
            await service.handle(user_password, db_user)

        # Verify exception details
        assert exc_info.value.blocked_until == blocked_until
        assert "blocked until" in str(exc_info.value).lower()

        # Verify updateSession was NOT called (blocked before password check)
        mock_session_repository.update_session_mock.assert_not_called()

    async def test_login_expired_block_allows_login(self, mock_session_repository):
        """Test that expired block allows successful login."""
        # Arrange
        user_id = AuthUserID(30)
        plain_password = "correct_password"
        hashed_password = AuthPassword.from_plain_text(plain_password)
        user_password = AuthPassword.keep_plain(plain_password)

        db_user = AuthUserDTO(
            user_id=user_id,
            email=AuthEmail("unblocked@example.com"),
            password=hashed_password,
        )

        # Mock session with expired block (in the past)
        blocked_until = datetime.now() - timedelta(minutes=1)
        existing_session = SessionDTO(
            user_id=user_id,
            token=None,
            failed_attempts=FailedLoginAttempts(4),
            blocked_until=BlockedTime(blocked_until),
        )
        mock_session_repository.get_session_mock.return_value = existing_session

        service = LoginService(mock_session_repository)

        # Act
        with patch.object(
            SessionToken, "generate", return_value=SessionToken("unblock-token")
        ):
            result = await service.handle(user_password, db_user)

        # Assert
        assert isinstance(result, SessionToken)
        assert result.value == "unblock-token"

        # Verify session was updated with reset attempts and cleared block
        updated_session = mock_session_repository.update_session_mock.call_args[0][0]
        assert updated_session.failed_attempts.value == 0
        assert updated_session.blocked_until is None
        assert updated_session.token.value == "unblock-token"

    async def test_successful_login_resets_failed_attempts(
        self, mock_session_repository
    ):
        """Test that successful login resets failed attempts counter."""
        # Arrange
        user_id = AuthUserID(35)
        plain_password = "correct_password"
        hashed_password = AuthPassword.from_plain_text(plain_password)
        user_password = AuthPassword.keep_plain(plain_password)

        db_user = AuthUserDTO(
            user_id=user_id,
            email=AuthEmail("reset@example.com"),
            password=hashed_password,
        )

        # Mock session with some failed attempts
        existing_session = SessionDTO(
            user_id=user_id,
            token=None,
            failed_attempts=FailedLoginAttempts(2),
            blocked_until=None,
        )
        mock_session_repository.get_session_mock.return_value = existing_session

        service = LoginService(mock_session_repository)

        # Act
        with patch.object(
            SessionToken, "generate", return_value=SessionToken("reset-token")
        ):
            result = await service.handle(user_password, db_user)

        # Assert
        assert isinstance(result, SessionToken)

        # Verify failed attempts were reset to 0
        updated_session = mock_session_repository.update_session_mock.call_args[0][0]
        assert updated_session.failed_attempts.value == 0
        assert updated_session.blocked_until is None
        assert updated_session.token is not None

    async def test_password_verification_called_correctly(
        self, mock_session_repository
    ):
        """Test that password verification is called with correct parameters."""
        # Arrange
        user_id = AuthUserID(40)
        plain_password = "test_password"
        hashed_password = AuthPassword.from_plain_text(plain_password)
        user_password = AuthPassword.keep_plain(plain_password)

        db_user = AuthUserDTO(
            user_id=user_id,
            email=AuthEmail("verify@example.com"),
            password=hashed_password,
        )

        existing_session = SessionDTO(
            user_id=user_id,
            token=None,
            failed_attempts=FailedLoginAttempts(0),
            blocked_until=None,
        )
        mock_session_repository.get_session_mock.return_value = existing_session

        service = LoginService(mock_session_repository)

        # Act
        with patch.object(
            SessionToken, "generate", return_value=SessionToken("verify-token")
        ):
            # Mock the password verify method to track calls
            with patch.object(AuthPassword, "verify", return_value=True) as mock_verify:
                await service.handle(user_password, db_user)

                # Verify password.verify was called with user_password.value
                mock_verify.assert_called_once_with(plain_password)

    async def test_session_token_generation(self, mock_session_repository):
        """Test that session token is generated on successful login."""
        # Arrange
        user_id = AuthUserID(45)
        plain_password = "password"
        hashed_password = AuthPassword.from_plain_text(plain_password)
        user_password = AuthPassword.keep_plain(plain_password)

        db_user = AuthUserDTO(
            user_id=user_id,
            email=AuthEmail("token@example.com"),
            password=hashed_password,
        )

        existing_session = SessionDTO(
            user_id=user_id,
            token=None,
            failed_attempts=FailedLoginAttempts(0),
            blocked_until=None,
        )
        mock_session_repository.get_session_mock.return_value = existing_session

        service = LoginService(mock_session_repository)

        # Act
        generated_token = SessionToken("unique-secure-token-xyz")
        with patch.object(
            SessionToken, "generate", return_value=generated_token
        ) as mock_generate:
            result = await service.handle(user_password, db_user)

            # Assert token generation was called
            mock_generate.assert_called_once()
            assert result == generated_token

    async def test_multiple_failed_attempts_sequence(self, mock_session_repository):
        """Test sequence of multiple failed login attempts."""
        # Arrange
        user_id = AuthUserID(50)
        correct_password = "correct"
        wrong_password = "wrong"
        hashed_password = AuthPassword.from_plain_text(correct_password)

        db_user = AuthUserDTO(
            user_id=user_id,
            email=AuthEmail("sequence@example.com"),
            password=hashed_password,
        )

        service = LoginService(mock_session_repository)

        # Test attempts 1-4
        for attempt in range(4):
            # Reset mock for each iteration
            mock_session_repository.update_session_mock.reset_mock()

            # Mock session with current attempt count
            existing_session = SessionDTO(
                user_id=user_id,
                token=None,
                failed_attempts=FailedLoginAttempts(attempt),
                blocked_until=None,
            )
            mock_session_repository.get_session_mock.return_value = existing_session

            user_password = AuthPassword.keep_plain(wrong_password)

            # Act & Assert
            with pytest.raises(InvalidCredentialsException):
                with patch("asyncio.sleep", new_callable=AsyncMock):
                    await service.handle(user_password, db_user)

            # Verify attempt count increased
            updated_session = mock_session_repository.update_session_mock.call_args[0][
                0
            ]
            assert updated_session.failed_attempts.value == attempt + 1

            # Check if blocked on 4th attempt
            if attempt + 1 >= 4:
                assert updated_session.blocked_until is not None
            else:
                assert updated_session.blocked_until is None
