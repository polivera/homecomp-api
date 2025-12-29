"""Unit tests for ThrottleTime value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.auth.domain.value_objects import FailedLoginAttempts
from app.context.auth.domain.value_objects.throttle_time import ThrottleTime


@pytest.mark.unit
class TestThrottleTime:
    """Tests for ThrottleTime value object"""

    def test_creation_with_direct_value(self):
        """Test creating ThrottleTime with direct value"""
        throttle = ThrottleTime(value=5)
        assert throttle.value == 5

    def test_from_attempts_zero_attempts(self):
        """Test that zero attempts results in 0 second throttle"""
        attempts = FailedLoginAttempts(0)
        throttle = ThrottleTime.fromAttempts(attempts)

        assert throttle.value == 0

    def test_from_attempts_one_attempt(self):
        """Test that one attempt results in 2 second throttle"""
        attempts = FailedLoginAttempts(1)
        throttle = ThrottleTime.fromAttempts(attempts)

        assert throttle.value == 2

    def test_from_attempts_two_attempts(self):
        """Test that two attempts results in 4 second throttle"""
        attempts = FailedLoginAttempts(2)
        throttle = ThrottleTime.fromAttempts(attempts)

        assert throttle.value == 4

    def test_from_attempts_three_attempts(self):
        """Test that three attempts results in 8 second throttle"""
        attempts = FailedLoginAttempts(3)
        throttle = ThrottleTime.fromAttempts(attempts)

        assert throttle.value == 8

    def test_throttle_time_tuple(self):
        """Test that throttle times match expected pattern"""
        # _throttleTimeSeconds = (0, 2, 4, 8)
        expected_times = [0, 2, 4, 8]

        for index, expected_time in enumerate(expected_times):
            attempts = FailedLoginAttempts(index)
            throttle = ThrottleTime.fromAttempts(attempts)
            assert throttle.value == expected_time

    def test_immutability(self):
        """Test that value object is immutable"""
        throttle = ThrottleTime(value=2)
        with pytest.raises(FrozenInstanceError):
            throttle.value = 4

    def test_equality(self):
        """Test that two ThrottleTime objects with same value are equal"""
        throttle1 = ThrottleTime(value=4)
        throttle2 = ThrottleTime(value=4)
        assert throttle1 == throttle2

    def test_inequality(self):
        """Test that two ThrottleTime objects with different values are not equal"""
        throttle1 = ThrottleTime(value=2)
        throttle2 = ThrottleTime(value=4)
        assert throttle1 != throttle2

    def test_progressive_throttling(self):
        """Test that throttle times increase with more attempts"""
        throttle_times = [
            ThrottleTime.fromAttempts(FailedLoginAttempts(i)).value for i in range(4)
        ]

        # Should be [0, 2, 4, 8]
        assert throttle_times == [0, 2, 4, 8]

        # Each should be greater than or equal to previous
        for i in range(1, len(throttle_times)):
            assert throttle_times[i] >= throttle_times[i - 1]
