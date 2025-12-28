"""Unit tests for CreditCardAccountID value object"""

import pytest

from app.context.credit_card.domain.value_objects import CreditCardAccountID


@pytest.mark.unit
class TestCreditCardAccountID:
    """Tests for CreditCardAccountID value object"""

    def test_valid_id_creation(self):
        """Test creating valid account IDs"""
        account_id = CreditCardAccountID(1)
        assert account_id.value == 1

    def test_invalid_type_raises_error(self):
        """Test that invalid types raise ValueError"""
        with pytest.raises(ValueError, match="AccountID must be an integer"):
            CreditCardAccountID("not_an_int")

    def test_negative_id_raises_error(self):
        """Test that negative IDs raise ValueError"""
        with pytest.raises(ValueError, match="AccountID must be positive"):
            CreditCardAccountID(-1)

    def test_zero_id_raises_error(self):
        """Test that zero ID raises ValueError"""
        with pytest.raises(ValueError, match="AccountID must be positive"):
            CreditCardAccountID(0)

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # This should work even with invalid data
        account_id = CreditCardAccountID.from_trusted_source(-999)
        assert account_id.value == -999

    def test_immutability(self):
        """Test that value object is immutable"""
        account_id = CreditCardAccountID(1)
        with pytest.raises(Exception):  # FrozenInstanceError
            account_id.value = 2
