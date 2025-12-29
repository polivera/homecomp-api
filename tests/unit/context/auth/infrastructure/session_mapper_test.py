"""Unit tests for SessionMapper"""

from datetime import datetime, timedelta

import pytest

from app.context.auth.domain.dto import SessionDTO
from app.context.auth.domain.value_objects import (
    AuthUserID,
    FailedLoginAttempts,
    SessionToken,
)
from app.context.auth.domain.value_objects.blocked_time import BlockedTime
from app.context.auth.infrastructure.mappers import SessionMapper
from app.context.auth.infrastructure.models import SessionModel


@pytest.mark.unit
class TestSessionMapper:
    """Tests for SessionMapper"""

    def test_to_dto_with_complete_session_model(self):
        """Test mapping complete SessionModel to SessionDTO"""
        # Arrange
        user_id = 42
        token_value = "test-token-123"
        failed_attempts = 2
        blocked_until = datetime.now() + timedelta(minutes=10)

        model = SessionModel(
            user_id=user_id,
            token=token_value,
            failed_attempts=failed_attempts,
            blocked_until=blocked_until,
        )

        # Act
        dto = SessionMapper.toDTO(model)

        # Assert
        assert dto is not None
        assert isinstance(dto, SessionDTO)
        assert dto.user_id.value == user_id
        assert dto.token.value == token_value
        assert dto.failed_attempts.value == failed_attempts
        assert dto.blocked_until.value == blocked_until

    def test_to_dto_with_none_token(self):
        """Test mapping SessionModel with None token"""
        # Arrange
        model = SessionModel(
            user_id=10,
            token=None,  # No token assigned yet
            failed_attempts=1,
            blocked_until=None,
        )

        # Act
        dto = SessionMapper.toDTO(model)

        # Assert
        assert dto is not None
        assert dto.user_id.value == 10
        assert dto.token is None
        assert dto.failed_attempts.value == 1
        assert dto.blocked_until is None

    def test_to_dto_with_none_blocked_until(self):
        """Test mapping SessionModel with None blocked_until"""
        # Arrange
        model = SessionModel(
            user_id=20,
            token="active-token",
            failed_attempts=0,
            blocked_until=None,  # Not blocked
        )

        # Act
        dto = SessionMapper.toDTO(model)

        # Assert
        assert dto is not None
        assert dto.user_id.value == 20
        assert dto.token.value == "active-token"
        assert dto.failed_attempts.value == 0
        assert dto.blocked_until is None

    def test_to_dto_with_none_model_returns_none(self):
        """Test that toDTO returns None when model is None"""
        # Act
        dto = SessionMapper.toDTO(None)

        # Assert
        assert dto is None

    def test_to_dto_creates_value_objects(self):
        """Test that toDTO creates proper value objects"""
        # Arrange
        model = SessionModel(
            user_id=99,
            token="value-object-token",
            failed_attempts=3,
            blocked_until=datetime(2025, 12, 25, 10, 0, 0),
        )

        # Act
        dto = SessionMapper.toDTO(model)

        # Assert
        assert isinstance(dto.user_id, AuthUserID)
        assert isinstance(dto.token, SessionToken)
        assert isinstance(dto.failed_attempts, FailedLoginAttempts)
        assert isinstance(dto.blocked_until, BlockedTime)

    def test_to_model_with_complete_session_dto(self):
        """Test mapping complete SessionDTO to SessionModel"""
        # Arrange
        user_id = AuthUserID(42)
        token = SessionToken("dto-token")
        failed_attempts = FailedLoginAttempts(2)
        blocked_until = BlockedTime(datetime(2025, 12, 25, 15, 30, 0))

        dto = SessionDTO(
            user_id=user_id,
            token=token,
            failed_attempts=failed_attempts,
            blocked_until=blocked_until,
        )

        # Act
        model = SessionMapper.toModel(dto)

        # Assert
        assert isinstance(model, SessionModel)
        assert model.user_id == 42
        assert model.token == "dto-token"
        assert model.failed_attempts == 2
        assert model.blocked_until == blocked_until  # BlockedTime object

    def test_to_model_with_none_token(self):
        """Test mapping SessionDTO with None token"""
        # Arrange
        dto = SessionDTO(
            user_id=AuthUserID(10),
            token=None,
            failed_attempts=FailedLoginAttempts(0),
            blocked_until=None,
        )

        # Act
        model = SessionMapper.toModel(dto)

        # Assert
        assert model.user_id == 10
        assert model.token is None
        assert model.failed_attempts == 0
        assert model.blocked_until is None

    def test_to_model_extracts_primitives(self):
        """Test that toModel extracts primitive values from value objects"""
        # Arrange
        dto = SessionDTO(
            user_id=AuthUserID(999),
            token=SessionToken("test-primitive-extraction"),
            failed_attempts=FailedLoginAttempts(4),
            blocked_until=None,
        )

        # Act
        model = SessionMapper.toModel(dto)

        # Assert
        # Verify primitives are extracted from value objects
        assert isinstance(model.user_id, int)
        assert isinstance(model.token, str)
        assert isinstance(model.failed_attempts, int)
        assert model.user_id == 999
        assert model.token == "test-primitive-extraction"
        assert model.failed_attempts == 4

    def test_round_trip_conversion(self):
        """Test that converting model -> dto -> model preserves data"""
        # Arrange
        blocked_datetime = datetime(2025, 12, 25, 12, 0, 0)
        original_model = SessionModel(
            user_id=123,
            token="round-trip-token",
            failed_attempts=2,
            blocked_until=blocked_datetime,
        )

        # Act
        dto = SessionMapper.toDTO(original_model)
        converted_model = SessionMapper.toModel(dto)

        # Assert
        assert converted_model.user_id == original_model.user_id
        assert converted_model.token == original_model.token
        assert converted_model.failed_attempts == original_model.failed_attempts
        # Note: toModel returns BlockedTime object, not datetime
        assert isinstance(converted_model.blocked_until, BlockedTime)
        assert converted_model.blocked_until.value == blocked_datetime

    def test_to_dto_with_zero_failed_attempts(self):
        """Test mapping with zero failed attempts"""
        # Arrange
        model = SessionModel(
            user_id=1,
            token="zero-attempts",
            failed_attempts=0,
            blocked_until=None,
        )

        # Act
        dto = SessionMapper.toDTO(model)

        # Assert
        assert dto.failed_attempts.value == 0
        assert dto.failed_attempts.hasReachMaxAttempts() is False

    def test_to_dto_with_max_failed_attempts(self):
        """Test mapping with max failed attempts (4)"""
        # Arrange
        model = SessionModel(
            user_id=1,
            token=None,
            failed_attempts=4,
            blocked_until=datetime.now() + timedelta(minutes=15),
        )

        # Act
        dto = SessionMapper.toDTO(model)

        # Assert
        assert dto.failed_attempts.value == 4
        assert dto.failed_attempts.hasReachMaxAttempts() is True

    def test_to_model_preserves_blocked_time_object(self):
        """Test that toModel preserves BlockedTime as an object"""
        # Arrange
        blocked_datetime = datetime(2025, 12, 25, 10, 0, 0)
        blocked_time = BlockedTime(blocked_datetime)

        dto = SessionDTO(
            user_id=AuthUserID(50),
            token=None,
            failed_attempts=FailedLoginAttempts(4),
            blocked_until=blocked_time,
        )

        # Act
        model = SessionMapper.toModel(dto)

        # Assert
        # Note: The mapper currently passes BlockedTime object directly
        # This matches the implementation in session_mapper.py line 36
        assert model.blocked_until == blocked_time
        assert isinstance(model.blocked_until, BlockedTime)
