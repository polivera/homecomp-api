"""Unit tests for UserAccountCurrency value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.user_account.domain.value_objects import UserAccountCurrency


@pytest.mark.unit
class TestUserAccountCurrency:
    """Tests for UserAccountCurrency value object"""

    def test_valid_currency_creation(self):
        """Test creating valid currencies"""
        currency = UserAccountCurrency("USD")
        assert currency.value == "USD"

    def test_three_letter_uppercase_required(self):
        """Test that currency must be 3 uppercase letters"""
        valid_currencies = ["USD", "EUR", "GBP", "JPY"]
        for curr in valid_currencies:
            currency = UserAccountCurrency(curr)
            assert currency.value == curr

    def test_lowercase_raises_error(self):
        """Test that lowercase currency codes raise ValueError"""
        with pytest.raises(ValueError, match="Currency code must be uppercase"):
            UserAccountCurrency("usd")

    def test_wrong_length_raises_error(self):
        """Test that non-3-character codes raise ValueError"""
        with pytest.raises(ValueError, match="Currency code must be exactly 3 characters"):
            UserAccountCurrency("US")

        with pytest.raises(ValueError, match="Currency code must be exactly 3 characters"):
            UserAccountCurrency("USDD")

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        currency = UserAccountCurrency.from_trusted_source("invalid")
        assert currency.value == "invalid"

    def test_immutability(self):
        """Test that value object is immutable"""
        currency = UserAccountCurrency("USD")
        with pytest.raises(FrozenInstanceError):
            currency.value = "EUR"
