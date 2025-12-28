"""Unit tests for user_account infrastructure mapper"""

import pytest
from decimal import Decimal
from datetime import datetime

from app.context.user_account.infrastructure.mappers.user_account_mapper import (
    UserAccountMapper,
)
from app.context.user_account.infrastructure.models.user_account_model import (
    UserAccountModel,
)
from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.value_objects import (
    UserAccountID,
    AccountName,
    UserAccountCurrency,
    UserAccountBalance,
    UserAccountUserID,
    UserAccountDeletedAt,
)
from app.context.user_account.domain.exceptions import UserAccountMapperError


@pytest.mark.unit
class TestUserAccountMapper:
    """Tests for UserAccountMapper"""

    def test_to_dto_converts_model_to_dto(self):
        """Test converting database model to domain DTO"""
        # Arrange
        model = UserAccountModel(
            id=10,
            user_id=1,
            name="My Account",
            currency="USD",
            balance=Decimal("100.50"),
            deleted_at=None,
        )

        # Act
        dto = UserAccountMapper.to_dto(model)

        # Assert
        assert dto is not None
        assert isinstance(dto, UserAccountDTO)
        assert dto.account_id.value == 10
        assert dto.user_id.value == 1
        assert dto.name.value == "My Account"
        assert dto.currency.value == "USD"
        assert dto.balance.value == Decimal("100.50")
        assert dto.deleted_at is None  # from_optional(None) returns None

    def test_to_dto_with_deleted_at(self):
        """Test converting model with deleted_at timestamp"""
        # Arrange
        now = datetime.now()
        model = UserAccountModel(
            id=10,
            user_id=1,
            name="Deleted Account",
            currency="USD",
            balance=Decimal("0.00"),
            deleted_at=now,
        )

        # Act
        dto = UserAccountMapper.to_dto(model)

        # Assert
        assert dto is not None
        assert dto.deleted_at.value == now
        assert dto.is_deleted is True

    def test_to_dto_with_none_model_returns_none(self):
        """Test that None model returns None DTO"""
        # Act
        dto = UserAccountMapper.to_dto(None)

        # Assert
        assert dto is None

    def test_to_dto_uses_trusted_source(self):
        """Test that to_dto uses from_trusted_source for performance"""
        # Arrange - create model with data that would fail validation
        # (empty name would normally fail AccountName validation)
        model = UserAccountModel(
            id=10,
            user_id=1,
            name="",  # Would fail validation if not using from_trusted_source
            currency="USD",
            balance=Decimal("100.00"),
            deleted_at=None,
        )

        # Act - should not raise because using from_trusted_source
        dto = UserAccountMapper.to_dto(model)

        # Assert
        assert dto is not None
        assert dto.name.value == ""  # Empty name preserved

    def test_to_dto_or_fail_with_valid_model(self):
        """Test to_dto_or_fail with valid model"""
        # Arrange
        model = UserAccountModel(
            id=10,
            user_id=1,
            name="My Account",
            currency="USD",
            balance=Decimal("100.00"),
            deleted_at=None,
        )

        # Act
        dto = UserAccountMapper.to_dto_or_fail(model)

        # Assert
        assert dto is not None
        assert isinstance(dto, UserAccountDTO)
        assert dto.account_id.value == 10

    def test_to_dto_or_fail_with_none_raises_error(self):
        """Test to_dto_or_fail raises error when DTO conversion results in None"""
        # When to_dto(None) is called, it returns None
        # to_dto_or_fail should raise UserAccountMapperError
        with pytest.raises(UserAccountMapperError, match="dto cannot be null"):
            UserAccountMapper.to_dto_or_fail(None)

    def test_to_model_converts_dto_to_model(self):
        """Test converting domain DTO to database model"""
        # Arrange
        dto = UserAccountDTO(
            account_id=UserAccountID(10),
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
            deleted_at=None,
        )

        # Act
        model = UserAccountMapper.to_model(dto)

        # Assert
        assert isinstance(model, UserAccountModel)
        assert model.id == 10
        assert model.user_id == 1
        assert model.name == "My Account"
        assert model.currency == "USD"
        assert model.balance == Decimal("100.50")
        assert model.deleted_at is None

    def test_to_model_with_none_account_id(self):
        """Test converting DTO without account_id (new entity)"""
        # Arrange
        dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("New Account"),
            currency=UserAccountCurrency("EUR"),
            balance=UserAccountBalance(Decimal("200.00")),
            account_id=None,  # New account, no ID yet
        )

        # Act
        model = UserAccountMapper.to_model(dto)

        # Assert
        assert model.id is None  # Will be assigned by database
        assert model.user_id == 1
        assert model.name == "New Account"
        assert model.currency == "EUR"

    def test_to_model_with_deleted_at(self):
        """Test converting DTO with deleted_at timestamp"""
        # Arrange
        from datetime import UTC
        now = datetime.now(UTC)
        dto = UserAccountDTO(
            account_id=UserAccountID(10),
            user_id=UserAccountUserID(1),
            name=AccountName("Deleted Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("0.00")),
            deleted_at=UserAccountDeletedAt.from_trusted_source(now),
        )

        # Act
        model = UserAccountMapper.to_model(dto)

        # Assert
        assert model.deleted_at == now

    def test_to_model_with_none_deleted_at(self):
        """Test converting DTO with None deleted_at"""
        # Arrange
        dto = UserAccountDTO(
            account_id=UserAccountID(10),
            user_id=UserAccountUserID(1),
            name=AccountName("Active Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.00")),
            deleted_at=None,
        )

        # Act
        model = UserAccountMapper.to_model(dto)

        # Assert
        assert model.deleted_at is None

    def test_roundtrip_conversion(self):
        """Test converting model to DTO and back to model"""
        # Arrange
        original_model = UserAccountModel(
            id=10,
            user_id=1,
            name="Test Account",
            currency="GBP",
            balance=Decimal("500.25"),
            deleted_at=None,
        )

        # Act - convert to DTO and back
        dto = UserAccountMapper.to_dto(original_model)
        final_model = UserAccountMapper.to_model(dto)

        # Assert - values should be preserved
        assert final_model.id == original_model.id
        assert final_model.user_id == original_model.user_id
        assert final_model.name == original_model.name
        assert final_model.currency == original_model.currency
        assert final_model.balance == original_model.balance
        assert final_model.deleted_at == original_model.deleted_at

    def test_to_model_preserves_decimal_precision(self):
        """Test that decimal precision is preserved during conversion"""
        # Arrange
        dto = UserAccountDTO(
            account_id=UserAccountID(10),
            user_id=UserAccountUserID(1),
            name=AccountName("Precision Test"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("99.99")),
        )

        # Act
        model = UserAccountMapper.to_model(dto)

        # Assert
        assert model.balance == Decimal("99.99")
        assert isinstance(model.balance, Decimal)
