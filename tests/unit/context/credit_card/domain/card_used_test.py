"""Unit tests for CardUsed value object"""

from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from app.context.credit_card.domain.exceptions import (
    InvalidCardUsedFormatError,
    InvalidCardUsedPrecisionError,
    InvalidCardUsedTypeError,
    InvalidCardUsedValueError,
)
from app.context.credit_card.domain.value_objects import CardUsed


@pytest.mark.unit
class TestCardUsed:
    """Tests for CardUsed value object"""

    def test_valid_used_creation(self):
        """Test creating valid card used amounts"""
        used = CardUsed(Decimal("500.00"))
        assert used.value == Decimal("500.00")

    def test_zero_used_is_valid(self):
        """Test that zero used amount is valid"""
        used = CardUsed(Decimal("0.00"))
        assert used.value == Decimal("0.00")

    def test_used_with_one_decimal_place(self):
        """Test used with one decimal place"""
        used = CardUsed(Decimal("250.5"))
        assert used.value == Decimal("250.5")

    def test_used_with_no_decimal_places(self):
        """Test used with no decimal places"""
        used = CardUsed(Decimal("500"))
        assert used.value == Decimal("500")

    def test_from_float_converts_correctly(self):
        """Test from_float class method"""
        used = CardUsed.from_float(123.45)
        assert used.value == Decimal("123.45")

    def test_from_float_rounds_to_two_decimals(self):
        """Test that from_float rounds to 2 decimal places"""
        used = CardUsed.from_float(123.456)
        assert used.value == Decimal("123.46")

    def test_invalid_type_raises_error(self):
        """Test that invalid types raise InvalidCardUsedTypeError"""
        with pytest.raises(
            InvalidCardUsedTypeError, match="CardUsed must be a Decimal"
        ):
            CardUsed(500)  # int instead of Decimal

    def test_negative_used_raises_error(self):
        """Test that negative used amounts raise InvalidCardUsedValueError"""
        with pytest.raises(
            InvalidCardUsedValueError, match="CardUsed must be non-negative"
        ):
            CardUsed(Decimal("-50.00"))

    def test_too_many_decimal_places_raises_error(self):
        """Test that more than 2 decimal places raises InvalidCardUsedPrecisionError"""
        with pytest.raises(
            InvalidCardUsedPrecisionError,
            match="CardUsed must have at most 2 decimal places",
        ):
            CardUsed(Decimal("50.123"))

    def test_from_float_with_invalid_value_raises_error(self):
        """Test that from_float with invalid value raises InvalidCardUsedFormatError"""
        with pytest.raises(InvalidCardUsedFormatError, match="Invalid CardUsed value"):
            CardUsed.from_float(float("nan"))

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # This should work even with invalid data
        used = CardUsed.from_trusted_source(Decimal("-50.123"))
        assert used.value == Decimal("-50.123")

    def test_immutability(self):
        """Test that value object is immutable"""
        used = CardUsed(Decimal("500.00"))
        with pytest.raises(FrozenInstanceError):
            used.value = Decimal("1000.00")
