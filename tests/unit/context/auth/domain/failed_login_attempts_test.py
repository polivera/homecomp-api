"""Unit tests for FailedLoginAttempts value object"""

import pytest

from app.context.auth.domain.value_objects import FailedLoginAttempts


@pytest.mark.unit
class TestFailedLoginAttempts:
    """Tests for FailedLoginAttempts value object"""

    def test_zero_attempts_creation(self):
        """Test creating attempts with zero value"""
        attempts = FailedLoginAttempts(0)
        assert attempts.value == 0

    def test_various_attempt_counts(self):
        """Test creating attempts with various values"""
        for count in [0, 1, 2, 3, 4, 5]:
            attempts = FailedLoginAttempts(count)
            assert attempts.value == count

    def test_has_reach_max_attempts_returns_false_below_max(self):
        """Test that hasReachMaxAttempts returns False below max"""
        # Max is 4, so 0-3 should return False
        for count in [0, 1, 2, 3]:
            attempts = FailedLoginAttempts(count)
            assert attempts.hasReachMaxAttempts() is False

    def test_has_reach_max_attempts_returns_true_at_max(self):
        """Test that hasReachMaxAttempts returns True at max (4)"""
        attempts = FailedLoginAttempts(4)
        assert attempts.hasReachMaxAttempts() is True

    def test_has_reach_max_attempts_returns_true_above_max(self):
        """Test that hasReachMaxAttempts returns True above max"""
        attempts = FailedLoginAttempts(5)
        assert attempts.hasReachMaxAttempts() is True

    def test_get_attempt_delay_first_attempt(self):
        """Test that first attempt (0) has no delay"""
        attempts = FailedLoginAttempts(0)
        assert attempts.getAttemptDelay() == 0

    def test_get_attempt_delay_second_attempt(self):
        """Test that second attempt (1) has no delay"""
        attempts = FailedLoginAttempts(1)
        assert attempts.getAttemptDelay() == 0

    def test_get_attempt_delay_third_attempt(self):
        """Test that third attempt (2) has 2 second delay"""
        attempts = FailedLoginAttempts(2)
        assert attempts.getAttemptDelay() == 2

    def test_get_attempt_delay_fourth_attempt(self):
        """Test that fourth attempt (3) has 4 second delay"""
        attempts = FailedLoginAttempts(3)
        assert attempts.getAttemptDelay() == 4

    def test_get_attempt_delay_beyond_max(self):
        """Test that attempts beyond max return 4 second delay"""
        # Attempts 4 and beyond should return 4 seconds
        for count in [4, 5, 10, 100]:
            attempts = FailedLoginAttempts(count)
            assert attempts.getAttemptDelay() == 4

    def test_reset_creates_zero_attempts(self):
        """Test that reset() creates FailedLoginAttempts with zero value"""
        attempts = FailedLoginAttempts.reset()
        assert attempts.value == 0
        assert attempts.hasReachMaxAttempts() is False
        assert attempts.getAttemptDelay() == 0

    def test_immutability(self):
        """Test that value object is immutable"""
        attempts = FailedLoginAttempts(2)
        with pytest.raises(Exception):  # FrozenInstanceError
            attempts.value = 3

    def test_equality(self):
        """Test that two FailedLoginAttempts with same value are equal"""
        attempts1 = FailedLoginAttempts(3)
        attempts2 = FailedLoginAttempts(3)
        assert attempts1 == attempts2

    def test_inequality(self):
        """Test that two FailedLoginAttempts with different values are not equal"""
        attempts1 = FailedLoginAttempts(1)
        attempts2 = FailedLoginAttempts(2)
        assert attempts1 != attempts2

    def test_progressive_delays(self):
        """Test that delays increase progressively"""
        delays = [FailedLoginAttempts(i).getAttemptDelay() for i in range(5)]

        # Delays should be: [0, 0, 2, 4, 4]
        assert delays == [0, 0, 2, 4, 4]

    def test_max_attempts_threshold(self):
        """Test the exact threshold for max attempts"""
        # Just below max
        attempts_3 = FailedLoginAttempts(3)
        assert attempts_3.hasReachMaxAttempts() is False

        # At max
        attempts_4 = FailedLoginAttempts(4)
        assert attempts_4.hasReachMaxAttempts() is True
