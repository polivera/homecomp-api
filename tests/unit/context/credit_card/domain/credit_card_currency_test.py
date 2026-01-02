"""Unit tests for CreditCardCurrency value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.credit_card.domain.value_objects import CreditCardCurrency


@pytest.mark.unit
class TestCreditCardCurrency:
    """Tests for CreditCardCurrency value object"""

    def test_valid_currency_creation(self):
        """Test creating valid currencies"""
        currency = CreditCardCurrency("USD")
        assert currency.value == "USD"

    def test_three_letter_uppercase_currency(self):
        """Test that 3-letter uppercase currencies are valid"""
        currencies = ["EUR", "GBP", "JPY", "CHF", "CAD"]
        for code in currencies:
            currency = CreditCardCurrency(code)
            assert currency.value == code

    def test_invalid_type_raises_error(self):
        """Test that invalid types raise ValueError"""
        with pytest.raises(ValueError, match="Currency must be a string"):
            CreditCardCurrency(123)

    def test_too_short_currency_raises_error(self):
        """Test that currency codes shorter than 3 characters raise error"""
        with pytest.raises(ValueError, match="Currency code must be exactly 3 characters"):
            CreditCardCurrency("US")

    def test_too_long_currency_raises_error(self):
        """Test that currency codes longer than 3 characters raise error"""
        with pytest.raises(ValueError, match="Currency code must be exactly 3 characters"):
            CreditCardCurrency("USDX")

    def test_lowercase_currency_raises_error(self):
        """Test that lowercase currency codes raise error"""
        with pytest.raises(ValueError, match="Currency code must be uppercase"):
            CreditCardCurrency("usd")

    def test_mixed_case_currency_raises_error(self):
        """Test that mixed case currency codes raise error"""
        with pytest.raises(ValueError, match="Currency code must be uppercase"):
            CreditCardCurrency("Usd")

    def test_currency_with_numbers_raises_error(self):
        """Test that currency codes with numbers raise error"""
        with pytest.raises(ValueError, match="Currency code must contain only letters"):
            CreditCardCurrency("US1")

    def test_currency_with_special_chars_raises_error(self):
        """Test that currency codes with special characters raise error"""
        with pytest.raises(ValueError, match="Currency code must contain only letters"):
            CreditCardCurrency("US$")

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # This should work even with invalid data
        currency = CreditCardCurrency.from_trusted_source("invalid")
        assert currency.value == "invalid"

    def test_immutability(self):
        """Test that value object is immutable"""
        currency = CreditCardCurrency("USD")
        with pytest.raises(FrozenInstanceError):
            currency.value = "EUR"
