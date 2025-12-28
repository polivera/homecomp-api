"""Unit tests for user_account domain DTOs"""

import pytest
from decimal import Decimal
from datetime import datetime

from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.value_objects import (
    UserAccountID,
    AccountName,
    UserAccountCurrency,
    UserAccountBalance,
    UserAccountUserID,
    UserAccountDeletedAt,
)


@pytest.mark.unit
class TestUserAccountDTO:
    """Tests for UserAccountDTO"""

    def test_create_dto_with_all_fields(self):
        """Test creating DTO with all fields populated"""
        from datetime import UTC
        now = datetime.now(UTC)
        dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
            account_id=UserAccountID(10),
            deleted_at=UserAccountDeletedAt.now(),
        )

        assert dto.user_id.value == 1
        assert dto.name.value == "My Account"
        assert dto.currency.value == "USD"
        assert dto.balance.value == Decimal("100.50")
        assert dto.account_id.value == 10
        assert isinstance(dto.deleted_at.value, datetime)

    def test_create_dto_without_optional_fields(self):
        """Test creating DTO without optional fields"""
        dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
        )

        assert dto.user_id.value == 1
        assert dto.name.value == "My Account"
        assert dto.currency.value == "USD"
        assert dto.balance.value == Decimal("100.50")
        assert dto.account_id is None
        assert dto.deleted_at is None

    def test_is_deleted_property_when_deleted(self):
        """Test is_deleted property returns True when deleted_at is set"""
        dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
            deleted_at=UserAccountDeletedAt.now(),
        )

        assert dto.is_deleted is True

    def test_is_deleted_property_when_not_deleted(self):
        """Test is_deleted property returns False when deleted_at is None"""
        dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
            deleted_at=None,
        )

        assert dto.is_deleted is False

    def test_is_deleted_property_with_none_deleted_at(self):
        """Test is_deleted property when deleted_at is None (using from_optional)"""
        # from_optional(None) returns None, not a DeletedAt object
        deleted_at_none = UserAccountDeletedAt.from_optional(None)

        dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
            deleted_at=deleted_at_none,  # This is None
        )

        # deleted_at is None, so is_deleted should be False
        assert dto.is_deleted is False

    def test_immutability(self):
        """Test that DTO is immutable"""
        dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
        )

        with pytest.raises(Exception):  # FrozenInstanceError
            dto.user_id = UserAccountUserID(2)

    def test_dto_with_negative_balance(self):
        """Test DTO with negative balance (overdraft)"""
        dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("Overdraft Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("-50.00")),
        )

        assert dto.balance.value == Decimal("-50.00")

    def test_dto_with_zero_balance(self):
        """Test DTO with zero balance"""
        dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("Empty Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("0.00")),
        )

        assert dto.balance.value == Decimal("0.00")

    def test_dto_equality(self):
        """Test that two DTOs with same values are equal"""
        dto1 = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
            account_id=UserAccountID(10),
        )

        dto2 = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
            account_id=UserAccountID(10),
        )

        assert dto1 == dto2

    def test_dto_inequality(self):
        """Test that DTOs with different values are not equal"""
        dto1 = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
        )

        dto2 = UserAccountDTO(
            user_id=UserAccountUserID(2),  # Different user_id
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
        )

        assert dto1 != dto2
