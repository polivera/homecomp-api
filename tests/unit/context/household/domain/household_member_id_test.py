"""Unit tests for HouseholdMemberID value object"""

import pytest

from app.context.household.domain.value_objects import HouseholdMemberID


@pytest.mark.unit
class TestHouseholdMemberID:
    """Tests for HouseholdMemberID value object"""

    def test_valid_id_creation(self):
        """Test creating valid household member ID"""
        member_id = HouseholdMemberID(1)
        assert member_id.value == 1

    def test_large_id_creation(self):
        """Test creating household member ID with large number"""
        member_id = HouseholdMemberID(999999)
        assert member_id.value == 999999

    def test_zero_id_raises_error(self):
        """Test that zero raises ValueError"""
        with pytest.raises(
            ValueError, match="Household member ID must be a positive integer"
        ):
            HouseholdMemberID(0)

    def test_negative_id_raises_error(self):
        """Test that negative number raises ValueError"""
        with pytest.raises(
            ValueError, match="Household member ID must be a positive integer"
        ):
            HouseholdMemberID(-1)

    def test_non_integer_raises_error(self):
        """Test that non-integer type raises ValueError"""
        with pytest.raises(ValueError, match="Household member ID must be an integer"):
            HouseholdMemberID("123")

    def test_float_raises_error(self):
        """Test that float raises ValueError"""
        with pytest.raises(ValueError, match="Household member ID must be an integer"):
            HouseholdMemberID(1.5)

    def test_immutability(self):
        """Test that value object is immutable"""
        member_id = HouseholdMemberID(1)
        with pytest.raises(Exception):  # FrozenInstanceError
            member_id.value = 2
