"""Unit tests for CreditCardUserID value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.credit_card.domain.value_objects import CreditCardUserID


@pytest.mark.unit
class TestCreditCardUserID:
    """Tests for CreditCardUserID value object"""

    def test_valid_id_creation(self):
        """Test creating valid user IDs"""
        user_id = CreditCardUserID(1)
        assert user_id.value == 1

    def test_large_id_creation(self):
        """Test creating large user IDs"""
        user_id = CreditCardUserID(999999)
        assert user_id.value == 999999

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        user_id = CreditCardUserID.from_trusted_source(12345)
        assert user_id.value == 12345

    def test_immutability(self):
        """Test that value object is immutable"""
        user_id = CreditCardUserID(1)
        with pytest.raises(FrozenInstanceError):
            user_id.value = 2
