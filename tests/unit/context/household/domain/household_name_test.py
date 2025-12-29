"""Unit tests for HouseholdName value object"""

import pytest

from app.context.household.domain.value_objects import HouseholdName


@pytest.mark.unit
class TestHouseholdName:
    """Tests for HouseholdName value object"""

    def test_valid_name_creation(self):
        """Test creating valid household name"""
        name = HouseholdName("My Household")
        assert name.value == "My Household"

    def test_single_character_name(self):
        """Test minimum length name"""
        name = HouseholdName("H")
        assert name.value == "H"

    def test_max_length_name(self):
        """Test maximum length name (100 characters)"""
        long_name = "H" * 100
        name = HouseholdName(long_name)
        assert name.value == long_name

    def test_name_with_special_characters(self):
        """Test name with special characters"""
        name = HouseholdName("Smith's Household #1")
        assert name.value == "Smith's Household #1"

    def test_empty_string_raises_error(self):
        """Test that empty string raises ValueError"""
        with pytest.raises(ValueError, match="Household name cannot be empty"):
            HouseholdName("")

    def test_whitespace_only_raises_error(self):
        """Test that whitespace-only string raises ValueError"""
        with pytest.raises(ValueError, match="Household name cannot be empty"):
            HouseholdName("   ")

    def test_tab_only_raises_error(self):
        """Test that tab-only string raises ValueError"""
        with pytest.raises(ValueError, match="Household name cannot be empty"):
            HouseholdName("\t")

    def test_exceeds_max_length_raises_error(self):
        """Test that names over 100 characters raise ValueError"""
        with pytest.raises(
            ValueError, match="Household name cannot exceed 100 characters"
        ):
            HouseholdName("H" * 101)

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # Should work even with empty string
        name = HouseholdName.from_trusted_source("")
        assert name.value == ""

        # Should work even with too long string
        long_name = "H" * 200
        name = HouseholdName.from_trusted_source(long_name)
        assert name.value == long_name

    def test_immutability(self):
        """Test that value object is immutable"""
        name = HouseholdName("Test")
        with pytest.raises(Exception):  # FrozenInstanceError
            name.value = "Changed"
