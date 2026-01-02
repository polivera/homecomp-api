"""Unit tests for CreditCardDeletedAt value object"""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta

import pytest

from app.context.credit_card.domain.value_objects import CreditCardDeletedAt


@pytest.mark.unit
class TestCreditCardDeletedAt:
    """Tests for CreditCardDeletedAt value object"""

    def test_valid_deleted_at_creation(self):
        """Test creating valid deleted_at timestamps"""
        now = datetime.now(UTC)
        deleted_at = CreditCardDeletedAt(now)
        assert deleted_at.value == now

    def test_past_datetime_is_valid(self):
        """Test that past datetime values are valid"""
        past = datetime.now(UTC) - timedelta(days=1)
        deleted_at = CreditCardDeletedAt(past)
        assert deleted_at.value == past

    def test_now_class_method(self):
        """Test the now() class method creates a current timestamp"""
        deleted_at = CreditCardDeletedAt.now()
        assert isinstance(deleted_at.value, datetime)
        assert deleted_at.value.tzinfo is not None  # Should be timezone-aware

    def test_future_datetime_raises_error(self):
        """Test that future datetime raises ValueError"""
        future = datetime.now(UTC) + timedelta(days=1)
        with pytest.raises(ValueError, match="DeletedAt cannot be in the future"):
            CreditCardDeletedAt(future)

    def test_invalid_type_raises_error(self):
        """Test that invalid types raise ValueError"""
        with pytest.raises(ValueError, match="DeletedAt must be a datetime object"):
            CreditCardDeletedAt("2025-01-01")

    def test_from_optional_with_none_returns_none(self):
        """Test that from_optional returns None when given None"""
        result = CreditCardDeletedAt.from_optional(None)
        assert result is None

    def test_from_optional_with_datetime_returns_deleted_at(self):
        """Test that from_optional returns DeletedAt when given datetime"""
        now = datetime.now(UTC)
        result = CreditCardDeletedAt.from_optional(now)
        assert isinstance(result, CreditCardDeletedAt)
        assert result.value == now

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # This should work even with invalid data (future date)
        future = datetime.now(UTC) + timedelta(days=100)
        deleted_at = CreditCardDeletedAt.from_trusted_source(future)
        assert deleted_at.value == future

    def test_immutability(self):
        """Test that value object is immutable"""
        deleted_at = CreditCardDeletedAt.now()
        with pytest.raises(FrozenInstanceError):
            deleted_at.value = datetime.now(UTC)
