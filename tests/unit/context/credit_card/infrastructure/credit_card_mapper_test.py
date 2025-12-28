"""Unit tests for CreditCardMapper"""

import pytest
from decimal import Decimal
from datetime import UTC, datetime

from app.context.credit_card.infrastructure.mappers.credit_card_mapper import (
    CreditCardMapper,
)
from app.context.credit_card.infrastructure.models import CreditCardModel
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
from app.context.credit_card.domain.exceptions import CreditCardMapperError


@pytest.mark.unit
class TestCreditCardMapper:
    """Tests for CreditCardMapper"""

    @pytest.fixture
    def sample_model(self):
        """Create a sample credit card model"""
        return CreditCardModel(
            id=1,
            user_id=100,
            account_id=10,
            name="My Credit Card",
            currency="USD",
            limit=Decimal("5000.00"),
            used=Decimal("1500.50"),
            deleted_at=None,
        )

    @pytest.fixture
    def sample_dto(self):
        """Create a sample credit card DTO"""
        return CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Credit Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("5000.00")),
            used=CardUsed(Decimal("1500.50")),
            deleted_at=None,
        )

    def test_to_dto_converts_model_to_dto(self, sample_model):
        """Test converting model to DTO"""
        dto = CreditCardMapper.to_dto(sample_model)

        assert dto is not None
        assert dto.credit_card_id.value == 1
        assert dto.user_id.value == 100
        assert dto.account_id.value == 10
        assert dto.name.value == "My Credit Card"
        assert dto.currency.value == "USD"
        assert dto.limit.value == Decimal("5000.00")
        assert dto.used.value == Decimal("1500.50")
        assert dto.deleted_at is None

    def test_to_dto_with_none_returns_none(self):
        """Test that to_dto returns None when given None"""
        dto = CreditCardMapper.to_dto(None)
        assert dto is None

    def test_to_dto_with_deleted_at(self):
        """Test converting model with deleted_at to DTO"""
        deleted_time = datetime.now(UTC)
        model = CreditCardModel(
            id=1,
            user_id=100,
            account_id=10,
            name="Deleted Card",
            currency="USD",
            limit=Decimal("1000.00"),
            used=Decimal("0.00"),
            deleted_at=deleted_time,
        )

        dto = CreditCardMapper.to_dto(model)

        assert dto is not None
        assert dto.deleted_at is not None
        assert dto.deleted_at.value == deleted_time
        assert dto.is_deleted is True

    def test_to_dto_with_zero_used(self):
        """Test converting model with zero used amount"""
        model = CreditCardModel(
            id=1,
            user_id=100,
            account_id=10,
            name="New Card",
            currency="EUR",
            limit=Decimal("2000.00"),
            used=Decimal("0.00"),
            deleted_at=None,
        )

        dto = CreditCardMapper.to_dto(model)

        assert dto is not None
        assert dto.used.value == Decimal("0.00")

    def test_to_dto_or_fail_success(self, sample_model):
        """Test to_dto_or_fail with valid model"""
        dto = CreditCardMapper.to_dto_or_fail(sample_model)

        assert dto is not None
        assert dto.credit_card_id.value == 1
        assert dto.name.value == "My Credit Card"

    def test_to_dto_or_fail_raises_error_on_none(self):
        """Test that to_dto_or_fail raises CreditCardMapperError on None"""
        with pytest.raises(CreditCardMapperError, match="Credit card dto cannot be null"):
            CreditCardMapper.to_dto_or_fail(None)

    def test_to_model_converts_dto_to_model(self, sample_dto):
        """Test converting DTO to model"""
        model = CreditCardMapper.to_model(sample_dto)

        assert model.id == 1
        assert model.user_id == 100
        assert model.account_id == 10
        assert model.name == "My Credit Card"
        assert model.currency == "USD"
        assert model.limit == Decimal("5000.00")
        assert model.used == Decimal("1500.50")
        assert model.deleted_at is None

    def test_to_model_with_none_credit_card_id(self):
        """Test converting DTO with None credit_card_id (new card)"""
        dto = CreditCardDTO(
            credit_card_id=None,  # New card
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("New Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
            used=CardUsed(Decimal("0.00")),
        )

        model = CreditCardMapper.to_model(dto)

        assert model.id is None
        assert model.name == "New Card"

    def test_to_model_with_none_used(self):
        """Test converting DTO with None used amount"""
        dto = CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
            used=None,  # No usage yet
        )

        model = CreditCardMapper.to_model(dto)

        assert model.used == 0  # Defaults to 0

    def test_to_model_with_deleted_at(self):
        """Test converting DTO with deleted_at to model"""
        deleted_time = datetime.now(UTC)
        dto = CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("Deleted Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
            deleted_at=CreditCardDeletedAt.from_trusted_source(deleted_time),
        )

        model = CreditCardMapper.to_model(dto)

        assert model.deleted_at == deleted_time

    def test_roundtrip_conversion(self, sample_model):
        """Test converting model -> DTO -> model maintains data"""
        dto = CreditCardMapper.to_dto(sample_model)
        model = CreditCardMapper.to_model(dto)

        assert model.id == sample_model.id
        assert model.user_id == sample_model.user_id
        assert model.account_id == sample_model.account_id
        assert model.name == sample_model.name
        assert model.currency == sample_model.currency
        assert model.limit == sample_model.limit
        assert model.used == sample_model.used
        assert model.deleted_at == sample_model.deleted_at

    def test_to_dto_uses_from_trusted_source(self, sample_model):
        """Test that to_dto uses from_trusted_source to skip validation"""
        # This model would fail validation if not using from_trusted_source
        # (e.g., name too short), but should work because mapper uses trusted source
        model = CreditCardModel(
            id=1,
            user_id=100,
            account_id=10,
            name="AB",  # Too short for normal validation
            currency="USD",
            limit=Decimal("1000.00"),
            used=Decimal("0.00"),
            deleted_at=None,
        )

        # Should not raise because mapper uses from_trusted_source
        dto = CreditCardMapper.to_dto(model)
        assert dto is not None
        assert dto.name.value == "AB"
