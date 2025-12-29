"""Unit tests for HouseholdUserName value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.household.domain.value_objects import HouseholdUserName


@pytest.mark.unit
class TestHouseholdUserName:
    """Tests for HouseholdUserName value object"""

    def test_valid_username_creation(self):
        """Test creating valid household username"""
        username = HouseholdUserName("john_doe")
        assert username.value == "john_doe"

    def test_username_with_special_characters(self):
        """Test username with special characters"""
        username = HouseholdUserName("user@example.com")
        assert username.value == "user@example.com"

    def test_numeric_username(self):
        """Test username with numbers"""
        username = HouseholdUserName("user123")
        assert username.value == "user123"

    def test_immutability(self):
        """Test that value object is immutable"""
        username = HouseholdUserName("test_user")
        with pytest.raises(FrozenInstanceError):
            username.value = "changed"
