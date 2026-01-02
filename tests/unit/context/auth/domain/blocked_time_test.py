"""Unit tests for BlockedTime value object"""

from datetime import datetime, timedelta

import pytest

from app.context.auth.domain.value_objects.blocked_time import BlockedTime


@pytest.mark.unit
class TestBlockedTime:
    """Tests for BlockedTime value object"""

    def test_creation_with_datetime(self):
        """Test creating BlockedTime with specific datetime"""
        future_time = datetime.now() + timedelta(minutes=10)
        blocked_time = BlockedTime(future_time)

        assert blocked_time.value == future_time

    def test_set_blocked_creates_future_time(self):
        """Test that setBlocked creates a time 15 minutes in the future"""
        before = datetime.now()
        blocked_time = BlockedTime.setBlocked()
        after = datetime.now()

        # Blocked time should be approximately 15 minutes from now
        expected_min = before + timedelta(minutes=14, seconds=55)
        expected_max = after + timedelta(minutes=15, seconds=5)

        assert expected_min <= blocked_time.value <= expected_max

    def test_set_blocked_uses_correct_duration(self):
        """Test that setBlocked uses BLOCK_MINUTES constant"""
        blocked_time = BlockedTime.setBlocked()
        now = datetime.now()

        # Should be approximately BLOCK_MINUTES (15) in the future
        time_diff = blocked_time.value - now
        assert 14.9 <= time_diff.total_seconds() / 60 <= 15.1

    def test_is_over_returns_false_for_future_time(self):
        """Test that isOver returns False when block is still active"""
        future_time = datetime.now() + timedelta(minutes=10)
        blocked_time = BlockedTime(future_time)

        assert blocked_time.isOver() is False

    def test_is_over_returns_true_for_past_time(self):
        """Test that isOver returns True when block has expired"""
        past_time = datetime.now() - timedelta(minutes=10)
        blocked_time = BlockedTime(past_time)

        assert blocked_time.isOver() is True

    def test_is_over_returns_true_for_current_time(self):
        """Test that isOver returns True for time that just passed"""
        # This is a race condition test - time just before now should be over
        almost_now = datetime.now() - timedelta(microseconds=1)
        blocked_time = BlockedTime(almost_now)

        assert blocked_time.isOver() is True

    def test_to_string_returns_iso_format(self):
        """Test that toString returns ISO formatted datetime string"""
        test_time = datetime(2025, 12, 25, 15, 30, 45)
        blocked_time = BlockedTime(test_time)

        iso_string = blocked_time.toString()

        assert isinstance(iso_string, str)
        assert iso_string == test_time.isoformat()

    def test_to_string_can_be_parsed_back(self):
        """Test that toString output can be parsed back to datetime"""
        original_time = datetime.now()
        blocked_time = BlockedTime(original_time)

        iso_string = blocked_time.toString()
        parsed_time = datetime.fromisoformat(iso_string)

        # Times should be equal (accounting for microseconds)
        assert abs((parsed_time - original_time).total_seconds()) < 0.001

    def test_block_minutes_constant(self):
        """Test that BLOCK_MINUTES constant is set correctly"""
        assert BlockedTime.BLOCK_MINUTES == 15

    def test_equality(self):
        """Test that two BlockedTime objects with same value are equal"""
        time_value = datetime(2025, 12, 25, 10, 0, 0)
        blocked1 = BlockedTime(time_value)
        blocked2 = BlockedTime(time_value)

        assert blocked1 == blocked2

    def test_inequality(self):
        """Test that two BlockedTime objects with different values are not equal"""
        time1 = datetime(2025, 12, 25, 10, 0, 0)
        time2 = datetime(2025, 12, 25, 11, 0, 0)
        blocked1 = BlockedTime(time1)
        blocked2 = BlockedTime(time2)

        assert blocked1 != blocked2

    def test_expired_block_scenario(self):
        """Test a complete scenario: block set, time passes, becomes expired"""
        # Set a block for 15 minutes
        blocked_time = BlockedTime.setBlocked()

        # Should not be over now
        assert blocked_time.isOver() is False

        # Simulate time passing (create new block in the past)
        past_block = BlockedTime(datetime.now() - timedelta(seconds=1))

        # Should be over
        assert past_block.isOver() is True

    def test_active_block_scenario(self):
        """Test a complete scenario: block is still active"""
        # Create block that expires 5 minutes from now
        future_block = BlockedTime(datetime.now() + timedelta(minutes=5))

        # Should not be over
        assert future_block.isOver() is False

        # ISO string should be a future time
        iso_string = future_block.toString()
        assert iso_string is not None
        assert len(iso_string) > 0
