"""Unit tests for EntryDescription value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.entry.domain.value_objects import EntryDescription


@pytest.mark.unit
class TestEntryDescription:
    """Tests for EntryDescription value object"""

    def test_valid_description_creation(self):
        """Test creating valid entry description"""
        description = EntryDescription("Grocery shopping at Whole Foods")
        assert description.value == "Grocery shopping at Whole Foods"

    def test_empty_string_is_valid(self):
        """Test that empty string is accepted"""
        description = EntryDescription("")
        assert description.value == ""

    def test_maximum_length_description(self):
        """Test that maximum length (500 characters) is accepted"""
        long_description = "A" * 500
        description = EntryDescription(long_description)
        assert description.value == long_description
        assert len(description.value) == 500

    def test_description_with_special_characters(self):
        """Test description with special characters"""
        description = EntryDescription("Payment for rent - $1,500.00 (Dec 2024)")
        assert description.value == "Payment for rent - $1,500.00 (Dec 2024)"

    def test_description_with_unicode(self):
        """Test description with unicode characters"""
        description = EntryDescription("Café lunch €15.50")
        assert description.value == "Café lunch €15.50"

    def test_invalid_type_raises_error(self):
        """Test that invalid types raise ValueError"""
        with pytest.raises(ValueError, match="EntryDescription must be a string"):
            EntryDescription(123)

    def test_invalid_type_none_raises_error(self):
        """Test that None raises ValueError"""
        with pytest.raises(ValueError, match="EntryDescription must be a string"):
            EntryDescription(None)

    def test_too_long_description_raises_error(self):
        """Test that descriptions longer than 500 characters raise error"""
        long_description = "A" * 501
        with pytest.raises(
            ValueError,
            match="EntryDescription cannot exceed 500 characters, got 501",
        ):
            EntryDescription(long_description)

    def test_very_long_description_raises_error(self):
        """Test that very long descriptions raise error"""
        very_long_description = "A" * 1000
        with pytest.raises(
            ValueError,
            match="EntryDescription cannot exceed 500 characters, got 1000",
        ):
            EntryDescription(very_long_description)

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # This should work even with invalid data
        description = EntryDescription.from_trusted_source("A" * 501)  # Too long
        assert description.value == "A" * 501

    def test_from_trusted_source_with_non_string(self):
        """Test that from_trusted_source even works with non-string (for DB data)"""
        # This bypasses validation entirely
        description = EntryDescription.from_trusted_source(123)
        assert description.value == 123

    def test_immutability(self):
        """Test that value object is immutable"""
        description = EntryDescription("Immutable description")
        with pytest.raises(FrozenInstanceError):
            description.value = "New description"
