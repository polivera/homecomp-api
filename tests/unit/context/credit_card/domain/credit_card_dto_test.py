"""Unit tests for CreditCardDTO"""

import pytest
from decimal import Decimal
from datetime import UTC, datetime

from app.context.credit_card.domain.dto import CreditCardDTO
from app.context.credit_card.domain.value_objects import (
    CardLimit,
    CardUsed,
    CreditCardAccountID,
    CreditCardCurrency,
    CreditCardDeletedAt,
    CreditCardID,
    CreditCardName,
    CreditCardUserID,
)


@pytest.mark.unit
class TestCreditCardDTO:
    """Tests for CreditCardDTO"""

    def test_minimal_dto_creation(self):
        """Test creating DTO with minimal required fields"""
        dto = CreditCardDTO(
            user_id=CreditCardUserID(1),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
        )

        assert dto.user_id.value == 1
        assert dto.account_id.value == 10
        assert dto.name.value == "My Card"
        assert dto.currency.value == "USD"
        assert dto.limit.value == Decimal("1000.00")
        assert dto.used is None
        assert dto.credit_card_id is None
        assert dto.deleted_at is None

    def test_full_dto_creation(self):
        """Test creating DTO with all fields"""
        dto = CreditCardDTO(
            user_id=CreditCardUserID(1),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
            used=CardUsed(Decimal("500.00")),
            credit_card_id=CreditCardID(5),
            deleted_at=CreditCardDeletedAt.now(),
        )

        assert dto.user_id.value == 1
        assert dto.account_id.value == 10
        assert dto.name.value == "My Card"
        assert dto.currency.value == "USD"
        assert dto.limit.value == Decimal("1000.00")
        assert dto.used.value == Decimal("500.00")
        assert dto.credit_card_id.value == 5
        assert dto.deleted_at is not None

    def test_is_deleted_property_when_deleted(self):
        """Test is_deleted property returns True when deleted_at is set"""
        dto = CreditCardDTO(
            user_id=CreditCardUserID(1),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
            deleted_at=CreditCardDeletedAt.now(),
        )

        assert dto.is_deleted is True

    def test_is_deleted_property_when_not_deleted(self):
        """Test is_deleted property returns False when deleted_at is None"""
        dto = CreditCardDTO(
            user_id=CreditCardUserID(1),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
        )

        assert dto.is_deleted is False

    def test_immutability(self):
        """Test that DTO is immutable"""
        dto = CreditCardDTO(
            user_id=CreditCardUserID(1),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
        )

        with pytest.raises(Exception):  # FrozenInstanceError
            dto.name = CreditCardName("New Name")

    def test_zero_used_amount(self):
        """Test DTO with zero used amount"""
        dto = CreditCardDTO(
            user_id=CreditCardUserID(1),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
            used=CardUsed(Decimal("0.00")),
        )

        assert dto.used.value == Decimal("0.00")

    def test_different_currencies(self):
        """Test DTO with different currency codes"""
        currencies = ["USD", "EUR", "GBP", "JPY"]

        for currency_code in currencies:
            dto = CreditCardDTO(
                user_id=CreditCardUserID(1),
                account_id=CreditCardAccountID(10),
                name=CreditCardName("My Card"),
                currency=CreditCardCurrency(currency_code),
                limit=CardLimit(Decimal("1000.00")),
            )
            assert dto.currency.value == currency_code
