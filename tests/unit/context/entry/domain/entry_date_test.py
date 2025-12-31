"""Unit tests for EntryDate value object"""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timezone

import pytest

from app.context.entry.domain.value_objects import EntryDate


@pytest.mark.unit
class TestEntryDate:
    """Tests for EntryDate value object"""

    def test_valid_timezone_aware_datetime(self):
        """Test creating entry date with timezone-aware datetime"""
        dt = datetime(2024, 12, 31, 15, 30, 0, tzinfo=UTC)
        entry_date = EntryDate(dt)
        assert entry_date.value == dt

    def test_timezone_aware_with_offset(self):
        """Test timezone-aware datetime with specific offset"""
        from datetime import timedelta

        tz = timezone(timedelta(hours=-5))  # EST
        dt = datetime(2024, 6, 15, 10, 0, 0, tzinfo=tz)
        entry_date = EntryDate(dt)
        assert entry_date.value == dt
        assert entry_date.value.tzinfo is not None

    def test_timezone_naive_datetime_raises_error(self):
        """Test that timezone-naive datetime raises ValueError"""
        dt_naive = datetime(2024, 12, 31, 15, 30, 0)  # No timezone
        with pytest.raises(ValueError, match="must be timezone-aware"):
            EntryDate(dt_naive)

    def test_invalid_type_raises_error(self):
        """Test that non-datetime types raise ValueError"""
        with pytest.raises(ValueError, match="EntryDate must be a datetime object"):
            EntryDate("2024-12-31")

    def test_invalid_type_int_raises_error(self):
        """Test that integer raises ValueError"""
        with pytest.raises(ValueError, match="EntryDate must be a datetime object"):
            EntryDate(1234567890)

    def test_none_raises_error(self):
        """Test that None raises ValueError"""
        with pytest.raises(ValueError, match="EntryDate must be a datetime object"):
            EntryDate(None)

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # Should work even with timezone-naive datetime
        dt_naive = datetime(2024, 12, 31, 15, 30, 0)
        entry_date = EntryDate.from_trusted_source(dt_naive)
        assert entry_date.value == dt_naive

    def test_from_trusted_source_with_timezone_aware(self):
        """Test from_trusted_source with timezone-aware datetime"""
        dt = datetime(2024, 12, 31, 15, 30, 0, tzinfo=UTC)
        entry_date = EntryDate.from_trusted_source(dt)
        assert entry_date.value == dt

    def test_immutability(self):
        """Test that value object is immutable"""
        dt = datetime(2024, 12, 31, 15, 30, 0, tzinfo=UTC)
        entry_date = EntryDate(dt)
        with pytest.raises(FrozenInstanceError):
            entry_date.value = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)

    def test_past_date(self):
        """Test entry date in the past"""
        dt = datetime(2020, 1, 1, 0, 0, 0, tzinfo=UTC)
        entry_date = EntryDate(dt)
        assert entry_date.value == dt

    def test_future_date(self):
        """Test entry date in the future"""
        dt = datetime(2030, 12, 31, 23, 59, 59, tzinfo=UTC)
        entry_date = EntryDate(dt)
        assert entry_date.value == dt

    def test_current_datetime(self):
        """Test creating entry date with current datetime"""
        now = datetime.now(UTC)
        entry_date = EntryDate(now)
        assert entry_date.value == now
        assert entry_date.value.tzinfo is not None
