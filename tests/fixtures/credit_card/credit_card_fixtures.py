"""Test fixtures for credit card context"""

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
from app.context.credit_card.infrastructure.models import CreditCardModel


@pytest.fixture
def valid_credit_card_dto():
    """Create a valid credit card DTO for testing"""
    return CreditCardDTO(
        credit_card_id=CreditCardID(1),
        user_id=CreditCardUserID(100),
        account_id=CreditCardAccountID(10),
        name=CreditCardName("Test Credit Card"),
        currency=CreditCardCurrency("USD"),
        limit=CardLimit(Decimal("5000.00")),
        used=CardUsed(Decimal("1500.50")),
        deleted_at=None,
    )


@pytest.fixture
def new_credit_card_dto():
    """Create a credit card DTO without ID (for creation tests)"""
    return CreditCardDTO(
        credit_card_id=None,  # New card
        user_id=CreditCardUserID(100),
        account_id=CreditCardAccountID(10),
        name=CreditCardName("New Card"),
        currency=CreditCardCurrency("EUR"),
        limit=CardLimit(Decimal("3000.00")),
        used=None,
        deleted_at=None,
    )


@pytest.fixture
def deleted_credit_card_dto():
    """Create a soft-deleted credit card DTO for testing"""
    return CreditCardDTO(
        credit_card_id=CreditCardID(2),
        user_id=CreditCardUserID(100),
        account_id=CreditCardAccountID(10),
        name=CreditCardName("Deleted Card"),
        currency=CreditCardCurrency("GBP"),
        limit=CardLimit(Decimal("2000.00")),
        used=CardUsed(Decimal("0.00")),
        deleted_at=CreditCardDeletedAt.now(),
    )


@pytest.fixture
def credit_card_model():
    """Create a credit card model for testing"""
    return CreditCardModel(
        id=1,
        user_id=100,
        account_id=10,
        name="Test Credit Card",
        currency="USD",
        limit=Decimal("5000.00"),
        used=Decimal("1500.50"),
        deleted_at=None,
    )


@pytest.fixture
def multiple_credit_card_dtos():
    """Create multiple credit card DTOs for list testing"""
    return [
        CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("Visa"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("5000.00")),
            used=CardUsed(Decimal("1500.00")),
        ),
        CreditCardDTO(
            credit_card_id=CreditCardID(2),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("Mastercard"),
            currency=CreditCardCurrency("EUR"),
            limit=CardLimit(Decimal("3000.00")),
            used=CardUsed(Decimal("500.00")),
        ),
        CreditCardDTO(
            credit_card_id=CreditCardID(3),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(11),
            name=CreditCardName("Amex"),
            currency=CreditCardCurrency("GBP"),
            limit=CardLimit(Decimal("10000.00")),
            used=CardUsed(Decimal("0.00")),
        ),
    ]


@pytest.fixture
def zero_used_credit_card_dto():
    """Create a credit card DTO with zero usage"""
    return CreditCardDTO(
        credit_card_id=CreditCardID(5),
        user_id=CreditCardUserID(100),
        account_id=CreditCardAccountID(10),
        name=CreditCardName("Unused Card"),
        currency=CreditCardCurrency("JPY"),
        limit=CardLimit(Decimal("100000.00")),
        used=CardUsed(Decimal("0.00")),
    )


@pytest.fixture
def maxed_out_credit_card_dto():
    """Create a credit card DTO at its limit"""
    limit_value = Decimal("2000.00")
    return CreditCardDTO(
        credit_card_id=CreditCardID(6),
        user_id=CreditCardUserID(100),
        account_id=CreditCardAccountID(10),
        name=CreditCardName("Maxed Card"),
        currency=CreditCardCurrency("USD"),
        limit=CardLimit(limit_value),
        used=CardUsed(limit_value),  # Same as limit
    )


# Helper functions

def create_credit_card_dto(
    card_id: int = 1,
    user_id: int = 100,
    account_id: int = 10,
    name: str = "Test Card",
    currency: str = "USD",
    limit: float = 5000.00,
    used: float = 0.00,
    deleted_at: datetime = None,
) -> CreditCardDTO:
    """
    Helper function to create a credit card DTO with custom values.

    Args:
        card_id: Credit card ID (None for new cards)
        user_id: User ID
        account_id: Account ID
        name: Card name
        currency: Currency code (3-letter)
        limit: Credit limit
        used: Used amount
        deleted_at: Deletion timestamp (None if not deleted)

    Returns:
        CreditCardDTO with specified values
    """
    return CreditCardDTO(
        credit_card_id=CreditCardID(card_id) if card_id else None,
        user_id=CreditCardUserID(user_id),
        account_id=CreditCardAccountID(account_id),
        name=CreditCardName(name),
        currency=CreditCardCurrency(currency),
        limit=CardLimit.from_float(limit),
        used=CardUsed.from_float(used) if used is not None else None,
        deleted_at=CreditCardDeletedAt.from_trusted_source(deleted_at) if deleted_at else None,
    )


def create_credit_card_model(
    card_id: int = 1,
    user_id: int = 100,
    account_id: int = 10,
    name: str = "Test Card",
    currency: str = "USD",
    limit: Decimal = Decimal("5000.00"),
    used: Decimal = Decimal("0.00"),
    deleted_at: datetime = None,
) -> CreditCardModel:
    """
    Helper function to create a credit card model with custom values.

    Args:
        card_id: Credit card ID
        user_id: User ID
        account_id: Account ID
        name: Card name
        currency: Currency code
        limit: Credit limit
        used: Used amount
        deleted_at: Deletion timestamp

    Returns:
        CreditCardModel with specified values
    """
    return CreditCardModel(
        id=card_id,
        user_id=user_id,
        account_id=account_id,
        name=name,
        currency=currency,
        limit=limit,
        used=used,
        deleted_at=deleted_at,
    )
