"""Unit tests for UserAccountBalance value object"""

import pytest
from decimal import Decimal

from app.context.user_account.domain.value_objects import UserAccountBalance


@pytest.mark.unit
class TestUserAccountBalance:
    """Tests for UserAccountBalance value object"""

    def test_valid_balance_creation(self):
        """Test creating valid balances"""
        balance = UserAccountBalance(Decimal("100.50"))
        assert balance.value == Decimal("100.50")

    def test_from_float_factory_method(self):
        """Test creating balance from float"""
        balance = UserAccountBalance.from_float(100.50)
        assert balance.value == Decimal("100.50")

    def test_zero_balance(self):
        """Test that zero balance is valid"""
        balance = UserAccountBalance(Decimal("0.00"))
        assert balance.value == Decimal("0.00")

    def test_negative_balance(self):
        """Test that negative balance is valid (for credit cards, overdrafts)"""
        balance = UserAccountBalance(Decimal("-50.00"))
        assert balance.value == Decimal("-50.00")

    def test_max_two_decimal_places(self):
        """Test that balance accepts max 2 decimal places"""
        balance = UserAccountBalance(Decimal("100.99"))
        assert balance.value == Decimal("100.99")

    def test_more_than_two_decimals_raises_error(self):
        """Test that more than 2 decimal places raise ValueError"""
        with pytest.raises(ValueError, match="Balance cannot have more than 2 decimal places"):
            UserAccountBalance(Decimal("100.999"))

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        balance = UserAccountBalance.from_trusted_source(Decimal("100.9999"))
        assert balance.value == Decimal("100.9999")

    def test_immutability(self):
        """Test that value object is immutable"""
        balance = UserAccountBalance(Decimal("100.00"))
        with pytest.raises(Exception):  # FrozenInstanceError
            balance.value = Decimal("200.00")
