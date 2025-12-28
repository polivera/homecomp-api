"""Unit tests for UserAccountDeletedAt value object"""

import pytest
from datetime import datetime, UTC

from app.context.user_account.domain.value_objects import UserAccountDeletedAt


@pytest.mark.unit
class TestUserAccountDeletedAt:
    """Tests for UserAccountDeletedAt value object"""

    def test_now_class_method(self):
        """Test the now() class method creates current timestamp"""
        deleted_at = UserAccountDeletedAt.now()
        assert isinstance(deleted_at.value, datetime)
        # Should be very recent (within 1 second)
        time_diff = datetime.now(UTC) - deleted_at.value
        assert time_diff.total_seconds() < 1

    def test_from_optional_with_value(self):
        """Test from_optional with non-None value"""
        now = datetime.now(UTC)
        deleted_at = UserAccountDeletedAt.from_optional(now)
        assert deleted_at is not None
        assert deleted_at.value == now

    def test_from_optional_with_none(self):
        """Test from_optional with None value returns None"""
        deleted_at = UserAccountDeletedAt.from_optional(None)
        assert deleted_at is None

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        future_date = datetime.now(UTC).replace(year=2099)
        # Should work even with future date when using from_trusted_source
        deleted_at = UserAccountDeletedAt.from_trusted_source(future_date)
        assert deleted_at.value == future_date

    def test_immutability(self):
        """Test that value object is immutable"""
        deleted_at = UserAccountDeletedAt.now()
        with pytest.raises(Exception):  # FrozenInstanceError
            deleted_at.value = datetime.now()
