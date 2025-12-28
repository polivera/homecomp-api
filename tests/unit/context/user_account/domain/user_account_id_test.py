"""Unit tests for UserAccountID value object"""

import pytest

from app.context.user_account.domain.value_objects import UserAccountID


@pytest.mark.unit
class TestUserAccountID:
    """Tests for UserAccountID value object"""

    def test_valid_id_creation(self):
        """Test creating valid account IDs"""
        account_id = UserAccountID(1)
        assert account_id.value == 1

    def test_invalid_type_raises_error(self):
        """Test that invalid types raise ValueError"""
        with pytest.raises(ValueError, match="AccountID must be an integer"):
            UserAccountID("not_an_int")

    def test_negative_id_raises_error(self):
        """Test that negative IDs raise ValueError"""
        with pytest.raises(ValueError, match="AccountID must be positive"):
            UserAccountID(-1)

    def test_zero_id_raises_error(self):
        """Test that zero ID raises ValueError"""
        with pytest.raises(ValueError, match="AccountID must be positive"):
            UserAccountID(0)

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # This should work even with invalid data
        account_id = UserAccountID.from_trusted_source(-999)
        assert account_id.value == -999

    def test_immutability(self):
        """Test that value object is immutable"""
        account_id = UserAccountID(1)
        with pytest.raises(Exception):  # FrozenInstanceError
            account_id.value = 2
