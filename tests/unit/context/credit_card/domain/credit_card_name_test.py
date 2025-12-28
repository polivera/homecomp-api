"""Unit tests for CreditCardName value object"""

import pytest

from app.context.credit_card.domain.value_objects import CreditCardName
from app.context.credit_card.domain.exceptions import (
    InvalidCreditCardNameTypeError,
    InvalidCreditCardNameLengthError,
)


@pytest.mark.unit
class TestCreditCardName:
    """Tests for CreditCardName value object"""

    def test_valid_name_creation(self):
        """Test creating valid credit card names"""
        name = CreditCardName("My Card")
        assert name.value == "My Card"

    def test_minimum_length_name(self):
        """Test that minimum length (3 characters) is accepted"""
        name = CreditCardName("Abc")
        assert name.value == "Abc"

    def test_maximum_length_name(self):
        """Test that maximum length (100 characters) is accepted"""
        long_name = "A" * 100
        name = CreditCardName(long_name)
        assert name.value == long_name

    def test_invalid_type_raises_error(self):
        """Test that invalid types raise InvalidCreditCardNameTypeError"""
        with pytest.raises(
            InvalidCreditCardNameTypeError, match="CreditCardName must be a string"
        ):
            CreditCardName(123)

    def test_too_short_name_raises_error(self):
        """Test that names shorter than 3 characters raise error"""
        with pytest.raises(
            InvalidCreditCardNameLengthError,
            match="CreditCardName must be at least 3 characters",
        ):
            CreditCardName("Ab")

    def test_too_long_name_raises_error(self):
        """Test that names longer than 100 characters raise error"""
        long_name = "A" * 101
        with pytest.raises(
            InvalidCreditCardNameLengthError,
            match="CreditCardName must be at most 100 characters",
        ):
            CreditCardName(long_name)

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # This should work even with invalid data
        name = CreditCardName.from_trusted_source("X")  # Too short
        assert name.value == "X"

    def test_immutability(self):
        """Test that value object is immutable"""
        name = CreditCardName("My Card")
        with pytest.raises(Exception):  # FrozenInstanceError
            name.value = "New Name"
