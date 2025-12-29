"""Unit tests for HouseholdID value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.household.domain.value_objects import HouseholdID


@pytest.mark.unit
class TestHouseholdID:
    """Tests for HouseholdID value object"""

    def test_valid_id_creation(self):
        """Test creating valid household ID"""
        household_id = HouseholdID(1)
        assert household_id.value == 1

    def test_large_id_creation(self):
        """Test creating household ID with large number"""
        household_id = HouseholdID(999999)
        assert household_id.value == 999999

    def test_zero_id_raises_error(self):
        """Test that zero raises ValueError"""
        with pytest.raises(ValueError, match="HouseholdID must be positive"):
            HouseholdID(0)

    def test_negative_id_raises_error(self):
        """Test that negative number raises ValueError"""
        with pytest.raises(ValueError, match="HouseholdID must be positive"):
            HouseholdID(-1)

    def test_non_integer_raises_error(self):
        """Test that non-integer type raises ValueError"""
        with pytest.raises(ValueError, match="HouseholdID must be an integer"):
            HouseholdID("123")

    def test_float_raises_error(self):
        """Test that float raises ValueError"""
        with pytest.raises(ValueError, match="HouseholdID must be an integer"):
            HouseholdID(1.5)

    def test_immutability(self):
        """Test that value object is immutable"""
        household_id = HouseholdID(1)
        with pytest.raises(FrozenInstanceError):
            household_id.value = 2
