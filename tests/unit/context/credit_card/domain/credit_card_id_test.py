"""Unit tests for CreditCardID value object"""

import pytest

from app.context.credit_card.domain.value_objects import CreditCardID
from app.context.credit_card.domain.exceptions import (
    InvalidCreditCardIdTypeError,
    InvalidCreditCardIdValueError,
)


@pytest.mark.unit
class TestCreditCardID:
    """Tests for CreditCardID value object"""

    def test_valid_id_creation(self):
        """Test creating valid credit card IDs"""
        card_id = CreditCardID(1)
        assert card_id.value == 1

    def test_invalid_type_raises_error(self):
        """Test that invalid types raise InvalidCreditCardIdTypeError"""
        with pytest.raises(
            InvalidCreditCardIdTypeError, match="CreditCardID must be an integer"
        ):
            CreditCardID("not_an_int")

    def test_negative_id_raises_error(self):
        """Test that negative IDs raise InvalidCreditCardIdValueError"""
        with pytest.raises(
            InvalidCreditCardIdValueError, match="CreditCardID must be positive"
        ):
            CreditCardID(-1)

    def test_zero_id_raises_error(self):
        """Test that zero ID raises InvalidCreditCardIdValueError"""
        with pytest.raises(
            InvalidCreditCardIdValueError, match="CreditCardID must be positive"
        ):
            CreditCardID(0)

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # This should work even with invalid data
        card_id = CreditCardID.from_trusted_source(-999)
        assert card_id.value == -999

    def test_immutability(self):
        """Test that value object is immutable"""
        card_id = CreditCardID(1)
        with pytest.raises(Exception):  # FrozenInstanceError
            card_id.value = 2
