from datetime import datetime, timedelta

import pytest

from app.context.auth.application.dto.get_session_result_dto import GetSessionResultDTO
from app.context.auth.application.handlers.get_session_handler import GetSessionHandler
from app.context.auth.application.queries import GetSessionQuery
from app.context.auth.domain.dto.session_dto import SessionDTO
from app.context.auth.domain.value_objects import (
    AuthUserID,
    FailedLoginAttempts,
    SessionToken,
)
from app.context.auth.domain.value_objects.blocked_time import BlockedTime


@pytest.mark.unit
@pytest.mark.asyncio
class TestGetSessionHandler:
    """Unit tests for GetSessionHandler."""

    async def test_handle_with_user_id_returns_session(self, mock_session_repository):
        """Test that handler returns session when found by user_id."""
        # Arrange
        user_id = 1
        token_value = "test-token-123"
        blocked_time = datetime.now() + timedelta(minutes=5)

        expected_session = SessionDTO(
            user_id=AuthUserID(user_id),
            token=SessionToken(token_value),
            failed_attempts=FailedLoginAttempts(2),
            blocked_until=BlockedTime(blocked_time),
        )

        mock_session_repository.get_session_mock.return_value = expected_session
        handler = GetSessionHandler(mock_session_repository)
        query = GetSessionQuery(user_id=user_id)

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is not None
        assert isinstance(result, GetSessionResultDTO)
        assert result.user_id == user_id
        assert result.token == token_value
        assert result.failed_attempts == 2
        assert result.blocked_until == blocked_time.isoformat()

        # Verify repository was called with correct parameters
        mock_session_repository.get_session_mock.assert_called_once()
        call_args = mock_session_repository.get_session_mock.call_args
        assert call_args.kwargs["user_id"] == AuthUserID(user_id)
        assert call_args.kwargs["token"] is None

    async def test_handle_with_token_returns_session(self, mock_session_repository):
        """Test that handler returns session when found by token."""
        # Arrange
        user_id = 42
        token_value = "secure-token-xyz"

        expected_session = SessionDTO(
            user_id=AuthUserID(user_id),
            token=SessionToken(token_value),
            failed_attempts=FailedLoginAttempts(0),
            blocked_until=None,
        )

        mock_session_repository.get_session_mock.return_value = expected_session
        handler = GetSessionHandler(mock_session_repository)
        query = GetSessionQuery(token=token_value)

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is not None
        assert isinstance(result, GetSessionResultDTO)
        assert result.user_id == user_id
        assert result.token == token_value
        assert result.failed_attempts == 0
        assert result.blocked_until is None

        # Verify repository was called with correct parameters
        mock_session_repository.get_session_mock.assert_called_once()
        call_args = mock_session_repository.get_session_mock.call_args
        assert call_args.kwargs["user_id"] is None
        assert call_args.kwargs["token"] == SessionToken(token_value)

    async def test_handle_with_both_user_id_and_token(self, mock_session_repository):
        """Test that handler works when both user_id and token are provided."""
        # Arrange
        user_id = 99
        token_value = "combined-token-456"

        expected_session = SessionDTO(
            user_id=AuthUserID(user_id),
            token=SessionToken(token_value),
            failed_attempts=FailedLoginAttempts(3),
            blocked_until=None,
        )

        mock_session_repository.get_session_mock.return_value = expected_session
        handler = GetSessionHandler(mock_session_repository)
        query = GetSessionQuery(user_id=user_id, token=token_value)

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is not None
        assert result.user_id == user_id
        assert result.token == token_value
        assert result.failed_attempts == 3

        # Verify both parameters were passed
        call_args = mock_session_repository.get_session_mock.call_args
        assert call_args.kwargs["user_id"] == AuthUserID(user_id)
        assert call_args.kwargs["token"] == SessionToken(token_value)

    async def test_handle_returns_none_when_session_not_found(self, mock_session_repository):
        """Test that handler returns None when repository returns None."""
        # Arrange
        mock_session_repository.get_session_mock.return_value = None
        handler = GetSessionHandler(mock_session_repository)
        query = GetSessionQuery(user_id=999)

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is None
        mock_session_repository.get_session_mock.assert_called_once()

    async def test_handle_with_no_token_in_session(self, mock_session_repository):
        """Test that handler correctly handles session with None token."""
        # Arrange
        user_id = 10

        expected_session = SessionDTO(
            user_id=AuthUserID(user_id),
            token=None,  # No token assigned yet
            failed_attempts=FailedLoginAttempts(1),
            blocked_until=None,
        )

        mock_session_repository.get_session_mock.return_value = expected_session
        handler = GetSessionHandler(mock_session_repository)
        query = GetSessionQuery(user_id=user_id)

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is not None
        assert result.user_id == user_id
        assert result.token is None
        assert result.failed_attempts == 1
        assert result.blocked_until is None

    async def test_handle_with_empty_query(self, mock_session_repository):
        """Test that handler works with empty query (both fields None)."""
        # Arrange
        mock_session_repository.get_session_mock.return_value = None
        handler = GetSessionHandler(mock_session_repository)
        query = GetSessionQuery()

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is None

        # Verify repository was called with None values
        call_args = mock_session_repository.get_session_mock.call_args
        assert call_args.kwargs["user_id"] is None
        assert call_args.kwargs["token"] is None

    async def test_handle_converts_value_objects_correctly(self, mock_session_repository):
        """Test that handler correctly converts domain value objects to primitives."""
        # Arrange
        user_id = 555
        token_value = "value-object-test-token"
        blocked_time = datetime(2025, 12, 25, 10, 30, 0)

        expected_session = SessionDTO(
            user_id=AuthUserID(user_id),
            token=SessionToken(token_value),
            failed_attempts=FailedLoginAttempts(4),
            blocked_until=BlockedTime(blocked_time),
        )

        mock_session_repository.get_session_mock.return_value = expected_session
        handler = GetSessionHandler(mock_session_repository)
        query = GetSessionQuery(user_id=user_id)

        # Act
        result = await handler.handle(query)

        # Assert
        # Verify all value objects are converted to primitives
        assert result is not None
        assert isinstance(result.user_id, int)
        assert isinstance(result.token, str)
        assert isinstance(result.failed_attempts, int)
        assert isinstance(result.blocked_until, str)
        assert result.blocked_until == blocked_time.isoformat()
