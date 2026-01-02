"""Unit tests for CardLimit value object"""

from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from app.context.credit_card.domain.exceptions import (
    InvalidCardLimitFormatError,
    InvalidCardLimitPrecisionError,
    InvalidCardLimitTypeError,
    InvalidCardLimitValueError,
)
from app.context.credit_card.domain.value_objects import CardLimit


@pytest.mark.unit
class TestCardLimit:
    """Tests for CardLimit value object"""

    def test_valid_limit_creation(self):
        """Test creating valid card limits"""
        limit = CardLimit(Decimal("1000.00"))
        assert limit.value == Decimal("1000.00")

    def test_limit_with_one_decimal_place(self):
        """Test limit with one decimal place"""
        limit = CardLimit(Decimal("500.5"))
        assert limit.value == Decimal("500.5")

    def test_limit_with_no_decimal_places(self):
        """Test limit with no decimal places"""
        limit = CardLimit(Decimal("1000"))
        assert limit.value == Decimal("1000")

    def test_from_float_converts_correctly(self):
        """Test from_float class method"""
        limit = CardLimit.from_float(1234.56)
        assert limit.value == Decimal("1234.56")

    def test_from_float_rounds_to_two_decimals(self):
        """Test that from_float rounds to 2 decimal places"""
        limit = CardLimit.from_float(1234.567)
        assert limit.value == Decimal("1234.57")

    def test_invalid_type_raises_error(self):
        """Test that invalid types raise InvalidCardLimitTypeError"""
        with pytest.raises(InvalidCardLimitTypeError, match="CardLimit must be a Decimal"):
            CardLimit(1000)  # int instead of Decimal

    def test_negative_limit_raises_error(self):
        """Test that negative limits raise InvalidCardLimitValueError"""
        with pytest.raises(InvalidCardLimitValueError, match="CardLimit must be positive"):
            CardLimit(Decimal("-100.00"))

    def test_zero_limit_raises_error(self):
        """Test that zero limit raises InvalidCardLimitValueError"""
        with pytest.raises(InvalidCardLimitValueError, match="CardLimit must be positive"):
            CardLimit(Decimal("0.00"))

    def test_too_many_decimal_places_raises_error(self):
        """Test that more than 2 decimal places raises InvalidCardLimitPrecisionError"""
        with pytest.raises(
            InvalidCardLimitPrecisionError,
            match="CardLimit must have at most 2 decimal places",
        ):
            CardLimit(Decimal("100.123"))

    def test_from_float_with_invalid_value_raises_error(self):
        """Test that from_float with invalid value raises InvalidCardLimitFormatError"""
        with pytest.raises(InvalidCardLimitFormatError, match="Invalid CardLimit value"):
            CardLimit.from_float(float("nan"))

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # This should work even with invalid data
        limit = CardLimit.from_trusted_source(Decimal("-100.123"))
        assert limit.value == Decimal("-100.123")

    def test_immutability(self):
        """Test that value object is immutable"""
        limit = CardLimit(Decimal("1000.00"))
        with pytest.raises(FrozenInstanceError):
            limit.value = Decimal("2000.00")
