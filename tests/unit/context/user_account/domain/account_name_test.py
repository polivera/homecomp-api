"""Unit tests for AccountName value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.user_account.domain.value_objects import AccountName


@pytest.mark.unit
class TestAccountName:
    """Tests for AccountName value object"""

    def test_valid_name_creation(self):
        """Test creating valid account names"""
        name = AccountName("My Account")
        assert name.value == "My Account"

    def test_single_character_name(self):
        """Test minimum length name"""
        name = AccountName("A")
        assert name.value == "A"

    def test_max_length_name(self):
        """Test maximum length name (100 characters)"""
        long_name = "A" * 100
        name = AccountName(long_name)
        assert name.value == long_name

    def test_empty_string_raises_error(self):
        """Test that empty string raises ValueError"""
        with pytest.raises(ValueError, match="AccountName cannot be empty or whitespace"):
            AccountName("")

    def test_whitespace_only_raises_error(self):
        """Test that whitespace-only string raises ValueError"""
        with pytest.raises(ValueError, match="AccountName cannot be empty or whitespace"):
            AccountName("   ")

    def test_exceeds_max_length_raises_error(self):
        """Test that names over 100 characters raise ValueError"""
        with pytest.raises(ValueError, match="AccountName cannot exceed 100 characters"):
            AccountName("A" * 101)

    def test_invalid_type_raises_error(self):
        """Test that non-string types raise ValueError"""
        with pytest.raises(ValueError, match="AccountName must be a string"):
            AccountName(123)

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # Should work even with empty string
        name = AccountName.from_trusted_source("")
        assert name.value == ""

    def test_immutability(self):
        """Test that value object is immutable"""
        name = AccountName("Test")
        with pytest.raises(FrozenInstanceError):
            name.value = "Changed"
