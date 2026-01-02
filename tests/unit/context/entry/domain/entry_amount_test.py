"""Unit tests for EntryAmount value object"""

from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from app.context.entry.domain.value_objects import EntryAmount


@pytest.mark.unit
class TestEntryAmount:
    """Tests for EntryAmount value object"""

    def test_valid_amount_from_decimal(self):
        """Test creating amount from Decimal"""
        amount = EntryAmount(Decimal("100.50"))
        assert amount.value == Decimal("100.50")

    def test_valid_amount_from_string_raises_error(self):
        """Test that strings raise ValueError"""
        with pytest.raises(ValueError, match="Amount must be a Decimal"):
            EntryAmount("250.75")

    def test_valid_amount_from_int_raises_error(self):
        """Test that integers raise ValueError"""
        with pytest.raises(ValueError, match="Amount must be a Decimal"):
            EntryAmount(1000)

    def test_valid_amount_from_float_raises_error(self):
        """Test that floats raise ValueError"""
        with pytest.raises(ValueError, match="Amount must be a Decimal"):
            EntryAmount(99.99)

    def test_zero_amount(self):
        """Test that zero amount is valid"""
        amount = EntryAmount(Decimal("0"))
        assert amount.value == Decimal("0")

    def test_negative_amount_raises_error(self):
        """Test that negative amounts raise ValueError"""
        with pytest.raises(ValueError, match="Amount must be non-negative"):
            EntryAmount(Decimal("-50.25"))

    def test_large_amount(self):
        """Test handling of large amounts"""
        large_amount = EntryAmount(Decimal("999999999.99"))
        assert large_amount.value == Decimal("999999999.99")

    def test_precision_limited_to_two_decimal_places(self):
        """Test that more than 2 decimal places raises ValueError"""
        with pytest.raises(ValueError, match="Amount cannot have more than 2 decimal places"):
            EntryAmount(Decimal("100.123"))

    def test_two_decimal_places(self):
        """Test amount with exactly 2 decimal places"""
        amount = EntryAmount(Decimal("50.00"))
        assert amount.value == Decimal("50.00")

    def test_invalid_type_raises_error(self):
        """Test that invalid types raise ValueError"""
        with pytest.raises(ValueError, match="Amount must be a Decimal"):
            EntryAmount("not-a-number")

    def test_none_raises_error(self):
        """Test that None raises ValueError"""
        with pytest.raises((ValueError, TypeError)):
            EntryAmount(None)

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # Should work even with pre-validated data
        amount = EntryAmount.from_trusted_source(Decimal("100.50"))
        assert amount.value == Decimal("100.50")

    def test_from_float_conversion(self):
        """Test from_float class method for safe float conversion"""
        amount = EntryAmount.from_float(123.45)
        assert amount.value == Decimal("123.45")

    def test_from_float_with_zero(self):
        """Test from_float with zero"""
        amount = EntryAmount.from_float(0.0)
        assert amount.value == Decimal("0")

    def test_from_float_with_negative_raises_error(self):
        """Test from_float with negative number raises error"""
        with pytest.raises(ValueError, match="Amount must be non-negative"):
            EntryAmount.from_float(-99.99)

    def test_immutability(self):
        """Test that value object is immutable"""
        amount = EntryAmount(Decimal("100.00"))
        with pytest.raises(FrozenInstanceError):
            amount.value = Decimal("200.00")
