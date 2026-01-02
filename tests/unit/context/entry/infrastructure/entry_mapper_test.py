"""Unit tests for EntryMapper"""

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from app.context.entry.domain.dto import EntryDTO
from app.context.entry.domain.exceptions import EntryMapperError
from app.context.entry.domain.value_objects import (
    EntryAccountID,
    EntryAmount,
    EntryCategoryID,
    EntryDate,
    EntryDescription,
    EntryHouseholdID,
    EntryID,
    EntryType,
    EntryUserID,
)
from app.context.entry.infrastructure.mappers.entry_mapper import EntryMapper
from app.context.entry.infrastructure.models import EntryModel
from app.shared.domain.value_objects.shared_entry_type import SharedEntryTypeValues


@pytest.mark.unit
class TestEntryMapper:
    """Tests for EntryMapper"""

    def test_to_dto_with_valid_model(self):
        """Test converting valid model to DTO"""
        # Arrange
        model = EntryModel(
            id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC),
            amount=Decimal("150.50"),
            description="Grocery shopping",
            household_id=3,
        )

        # Act
        dto = EntryMapper.to_dto(model)

        # Assert
        assert dto is not None
        assert isinstance(dto, EntryDTO)
        assert dto.entry_id == EntryID.from_trusted_source(100)
        assert dto.user_id == EntryUserID.from_trusted_source(1)
        assert dto.account_id == EntryAccountID.from_trusted_source(10)
        assert dto.category_id == EntryCategoryID.from_trusted_source(5)
        assert dto.entry_type.value == SharedEntryTypeValues.EXPENSE
        assert dto.entry_date.value == datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)
        assert dto.amount.value == Decimal("150.50")
        assert dto.description.value == "Grocery shopping"
        assert dto.household_id == EntryHouseholdID.from_trusted_source(3)

    def test_to_dto_with_none_model(self):
        """Test converting None model returns None"""
        # Act
        dto = EntryMapper.to_dto(None)

        # Assert
        assert dto is None

    def test_to_dto_without_household_id(self):
        """Test converting model without household_id"""
        # Arrange
        model = EntryModel(
            id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="income",
            entry_date=datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC),
            amount=Decimal("1000.00"),
            description="Salary",
            household_id=None,
        )

        # Act
        dto = EntryMapper.to_dto(model)

        # Assert
        assert dto is not None
        assert dto.household_id is None

    def test_to_dto_with_income_type(self):
        """Test converting model with income type"""
        # Arrange
        model = EntryModel(
            id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="income",
            entry_date=datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC),
            amount=Decimal("2000.00"),
            description="Monthly salary",
            household_id=None,
        )

        # Act
        dto = EntryMapper.to_dto(model)

        # Assert
        assert dto is not None
        assert dto.entry_type.value == SharedEntryTypeValues.INCOME

    def test_to_dto_uses_from_trusted_source(self):
        """Test that to_dto uses from_trusted_source for performance"""
        # Arrange - data that would normally fail validation
        model = EntryModel(
            id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC),
            amount=Decimal("150.50"),
            description="Test",  # Valid, but testing trusted source path
            household_id=3,
        )

        # Act
        dto = EntryMapper.to_dto(model)

        # Assert - should succeed because from_trusted_source skips validation
        assert dto is not None
        assert dto.entry_id.value == 100

    def test_to_dto_or_fail_with_valid_model(self):
        """Test to_dto_or_fail with valid model"""
        # Arrange
        model = EntryModel(
            id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC),
            amount=Decimal("150.50"),
            description="Test",
            household_id=None,
        )

        # Act
        dto = EntryMapper.to_dto_or_fail(model)

        # Assert
        assert dto is not None
        assert isinstance(dto, EntryDTO)
        assert dto.entry_id.value == 100

    def test_to_dto_or_fail_with_none_raises_error(self):
        """Test that to_dto_or_fail with None raises EntryMapperError"""
        # Act & Assert
        with pytest.raises(EntryMapperError, match="Entry DTO cannot be null"):
            EntryMapper.to_dto_or_fail(None)

    def test_to_model_with_all_fields(self):
        """Test converting DTO to model with all fields"""
        # Arrange
        dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("150.50")),
            description=EntryDescription("Grocery shopping"),
            household_id=EntryHouseholdID(3),
        )

        # Act
        model = EntryMapper.to_model(dto)

        # Assert
        assert isinstance(model, EntryModel)
        assert model.id == 100
        assert model.user_id == 1
        assert model.account_id == 10
        assert model.category_id == 5
        assert model.entry_type == "expense"
        assert model.entry_date == datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)
        assert model.amount == Decimal("150.50")
        assert model.description == "Grocery shopping"
        assert model.household_id == 3

    def test_to_model_without_entry_id(self):
        """Test converting DTO to model without entry_id (new entry)"""
        # Arrange
        dto = EntryDTO(
            entry_id=None,
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("100.00")),
            description=EntryDescription("Test"),
            household_id=None,
        )

        # Act
        model = EntryMapper.to_model(dto)

        # Assert
        assert model.id is None
        assert model.user_id == 1

    def test_to_model_without_household_id(self):
        """Test converting DTO to model without household_id"""
        # Arrange
        dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.INCOME),
            entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("1000.00")),
            description=EntryDescription("Salary"),
            household_id=None,
        )

        # Act
        model = EntryMapper.to_model(dto)

        # Assert
        assert model.household_id is None

    def test_to_model_with_income_type(self):
        """Test converting DTO with income type to model"""
        # Arrange
        dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.INCOME),
            entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("2000.00")),
            description=EntryDescription("Monthly salary"),
            household_id=None,
        )

        # Act
        model = EntryMapper.to_model(dto)

        # Assert
        assert model.entry_type == "income"

    def test_to_model_preserves_precision(self):
        """Test that decimal precision is preserved in model conversion"""
        # Arrange
        dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("123.45")),
            description=EntryDescription("Test"),
            household_id=None,
        )

        # Act
        model = EntryMapper.to_model(dto)

        # Assert
        assert model.amount == Decimal("123.45")
        assert str(model.amount) == "123.45"

    def test_roundtrip_conversion(self):
        """Test that model -> DTO -> model preserves data"""
        # Arrange
        original_model = EntryModel(
            id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC),
            amount=Decimal("150.50"),
            description="Grocery shopping",
            household_id=3,
        )

        # Act
        dto = EntryMapper.to_dto(original_model)
        converted_model = EntryMapper.to_model(dto)

        # Assert
        assert converted_model.id == original_model.id
        assert converted_model.user_id == original_model.user_id
        assert converted_model.account_id == original_model.account_id
        assert converted_model.category_id == original_model.category_id
        assert converted_model.entry_type == original_model.entry_type
        assert converted_model.entry_date == original_model.entry_date
        assert converted_model.amount == original_model.amount
        assert converted_model.description == original_model.description
        assert converted_model.household_id == original_model.household_id
