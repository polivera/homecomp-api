"""User account context test fixtures"""

from decimal import Decimal
from datetime import datetime
import pytest

from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.value_objects import (
    UserAccountID,
    AccountName,
    UserAccountCurrency,
    UserAccountBalance,
    UserAccountUserID,
    UserAccountDeletedAt,
)
from app.context.user_account.infrastructure.models.user_account_model import (
    UserAccountModel,
)


# ──────────────────────────────────────────────────────────────────────────────
# Domain Value Object Fixtures
# ──────────────────────────────────────────────────────────────────────────────


@pytest.fixture
def sample_user_id() -> UserAccountUserID:
    """Create a sample user ID"""
    return UserAccountUserID(1)


@pytest.fixture
def sample_account_id() -> UserAccountID:
    """Create a sample account ID"""
    return UserAccountID(10)


@pytest.fixture
def sample_account_name() -> AccountName:
    """Create a sample account name"""
    return AccountName("My Checking Account")


@pytest.fixture
def sample_currency() -> UserAccountCurrency:
    """Create a sample currency"""
    return UserAccountCurrency("USD")


@pytest.fixture
def sample_balance() -> UserAccountBalance:
    """Create a sample balance"""
    return UserAccountBalance(Decimal("1000.00"))


# ──────────────────────────────────────────────────────────────────────────────
# Domain DTO Fixtures
# ──────────────────────────────────────────────────────────────────────────────


@pytest.fixture
def sample_account_dto(
    sample_user_id: UserAccountUserID,
    sample_account_id: UserAccountID,
    sample_account_name: AccountName,
    sample_currency: UserAccountCurrency,
    sample_balance: UserAccountBalance,
) -> UserAccountDTO:
    """Create a sample UserAccountDTO"""
    return UserAccountDTO(
        user_id=sample_user_id,
        account_id=sample_account_id,
        name=sample_account_name,
        currency=sample_currency,
        balance=sample_balance,
        deleted_at=None,
    )


@pytest.fixture
def sample_new_account_dto(
    sample_user_id: UserAccountUserID,
    sample_account_name: AccountName,
    sample_currency: UserAccountCurrency,
    sample_balance: UserAccountBalance,
) -> UserAccountDTO:
    """Create a sample UserAccountDTO for a new account (no ID)"""
    return UserAccountDTO(
        user_id=sample_user_id,
        name=sample_account_name,
        currency=sample_currency,
        balance=sample_balance,
        account_id=None,
        deleted_at=None,
    )


@pytest.fixture
def sample_deleted_account_dto(
    sample_user_id: UserAccountUserID,
    sample_account_id: UserAccountID,
    sample_account_name: AccountName,
    sample_currency: UserAccountCurrency,
) -> UserAccountDTO:
    """Create a sample deleted UserAccountDTO"""
    return UserAccountDTO(
        user_id=sample_user_id,
        account_id=sample_account_id,
        name=sample_account_name,
        currency=sample_currency,
        balance=UserAccountBalance(Decimal("0.00")),
        deleted_at=UserAccountDeletedAt(datetime.now()),
    )


# ──────────────────────────────────────────────────────────────────────────────
# Infrastructure Model Fixtures
# ──────────────────────────────────────────────────────────────────────────────


@pytest.fixture
def sample_account_model() -> UserAccountModel:
    """Create a sample UserAccountModel"""
    return UserAccountModel(
        id=10,
        user_id=1,
        name="My Checking Account",
        currency="USD",
        balance=Decimal("1000.00"),
        deleted_at=None,
    )


@pytest.fixture
def sample_deleted_account_model() -> UserAccountModel:
    """Create a sample deleted UserAccountModel"""
    return UserAccountModel(
        id=10,
        user_id=1,
        name="Deleted Account",
        currency="USD",
        balance=Decimal("0.00"),
        deleted_at=datetime.now(),
    )


# Export all fixtures
__all__ = [
    "sample_user_id",
    "sample_account_id",
    "sample_account_name",
    "sample_currency",
    "sample_balance",
    "sample_account_dto",
    "sample_new_account_dto",
    "sample_deleted_account_dto",
    "sample_account_model",
    "sample_deleted_account_model",
]
