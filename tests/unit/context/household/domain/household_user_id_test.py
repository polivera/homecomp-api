"""Unit tests for HouseholdUserID value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.household.domain.value_objects import HouseholdUserID


@pytest.mark.unit
class TestHouseholdUserID:
    """Tests for HouseholdUserID value object"""

    def test_valid_id_creation(self):
        """Test creating valid household user ID"""
        user_id = HouseholdUserID(1)
        assert user_id.value == 1

    def test_large_id_creation(self):
        """Test creating household user ID with large number"""
        user_id = HouseholdUserID(999999)
        assert user_id.value == 999999

    def test_zero_id_raises_error(self):
        """Test that zero raises ValueError"""
        with pytest.raises(ValueError, match="HouseholdUserID must be positive"):
            HouseholdUserID(0)

    def test_negative_id_raises_error(self):
        """Test that negative number raises ValueError"""
        with pytest.raises(ValueError, match="HouseholdUserID must be positive"):
            HouseholdUserID(-1)

    def test_non_integer_raises_error(self):
        """Test that non-integer type raises ValueError"""
        with pytest.raises(ValueError, match="HouseholdUserID must be an integer"):
            HouseholdUserID("123")

    def test_float_raises_error(self):
        """Test that float raises ValueError"""
        with pytest.raises(ValueError, match="HouseholdUserID must be an integer"):
            HouseholdUserID(1.5)

    def test_immutability(self):
        """Test that value object is immutable"""
        user_id = HouseholdUserID(1)
        with pytest.raises(FrozenInstanceError):
            user_id.value = 2
