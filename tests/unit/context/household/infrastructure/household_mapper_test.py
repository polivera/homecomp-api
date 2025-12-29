"""Unit tests for HouseholdMapper"""

import pytest
from datetime import UTC, datetime

from app.context.household.infrastructure.mappers.household_mapper import HouseholdMapper
from app.context.household.infrastructure.models import HouseholdModel
from app.context.household.domain.dto import HouseholdDTO
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdName,
    HouseholdUserID,
)
from app.context.household.domain.exceptions import HouseholdMapperError


@pytest.mark.unit
class TestHouseholdMapper:
    """Tests for HouseholdMapper"""

    def test_to_dto_converts_model_to_dto(self):
        """Test converting database model to domain DTO"""
        # Arrange
        now = datetime.now(UTC)
        model = HouseholdModel(
            id=10,
            owner_user_id=1,
            name="Smith Family",
            created_at=now,
        )

        # Act
        dto = HouseholdMapper.to_dto(model)

        # Assert
        assert dto is not None
        assert isinstance(dto, HouseholdDTO)
        assert dto.household_id == HouseholdID(10)
        assert dto.owner_user_id == HouseholdUserID(1)
        assert dto.name.value == "Smith Family"
        assert dto.created_at == now

    def test_to_dto_with_none_model_returns_none(self):
        """Test that None model returns None DTO"""
        # Act
        dto = HouseholdMapper.to_dto(None)

        # Assert
        assert dto is None

    def test_to_dto_uses_trusted_source_for_name(self):
        """Test that to_dto uses from_trusted_source for performance"""
        # Arrange - create model with empty name that would fail validation
        model = HouseholdModel(
            id=10,
            owner_user_id=1,
            name="",  # Would fail validation if not using from_trusted_source
            created_at=datetime.now(UTC),
        )

        # Act - should not raise because using from_trusted_source
        dto = HouseholdMapper.to_dto(model)

        # Assert
        assert dto is not None
        assert dto.name.value == ""  # Empty name preserved

    def test_to_dto_or_fail_with_valid_model(self):
        """Test to_dto_or_fail with valid model"""
        # Arrange
        model = HouseholdModel(
            id=10,
            owner_user_id=1,
            name="Smith Family",
            created_at=datetime.now(UTC),
        )

        # Act
        dto = HouseholdMapper.to_dto_or_fail(model)

        # Assert
        assert dto is not None
        assert isinstance(dto, HouseholdDTO)
        assert dto.household_id == HouseholdID(10)

    def test_to_dto_or_fail_with_none_raises_error(self):
        """Test to_dto_or_fail raises error when model is None"""
        # Act & Assert
        with pytest.raises(HouseholdMapperError, match="Error mapping HouseholdModel to DTO"):
            HouseholdMapper.to_dto_or_fail(None)

    def test_to_model_converts_dto_to_model(self):
        """Test converting domain DTO to database model"""
        # Arrange
        now = datetime.now(UTC)
        dto = HouseholdDTO(
            household_id=HouseholdID(10),
            owner_user_id=HouseholdUserID(1),
            name=HouseholdName("Smith Family"),
            created_at=now,
        )

        # Act
        model = HouseholdMapper.to_model(dto)

        # Assert
        assert isinstance(model, HouseholdModel)
        assert model.id == 10
        assert model.owner_user_id == 1
        assert model.name == "Smith Family"
        assert model.created_at == now

    def test_to_model_with_none_household_id(self):
        """Test converting DTO without household_id (new entity)"""
        # Arrange
        dto = HouseholdDTO(
            household_id=None,  # New household, no ID yet
            owner_user_id=HouseholdUserID(1),
            name=HouseholdName("New Household"),
        )

        # Act
        model = HouseholdMapper.to_model(dto)

        # Assert
        # id attribute won't exist if household_id is None
        assert not hasattr(model, "id") or model.id is None
        assert model.owner_user_id == 1
        assert model.name == "New Household"

    def test_to_model_with_none_created_at(self):
        """Test converting DTO with None created_at"""
        # Arrange
        dto = HouseholdDTO(
            household_id=HouseholdID(10),
            owner_user_id=HouseholdUserID(1),
            name=HouseholdName("Test Household"),
            created_at=None,  # Will be set by database default
        )

        # Act
        model = HouseholdMapper.to_model(dto)

        # Assert
        # created_at won't be set if None in DTO (database will set it)
        assert not hasattr(model, "created_at") or model.created_at is None

    def test_roundtrip_conversion(self):
        """Test converting model to DTO and back to model"""
        # Arrange
        now = datetime.now(UTC)
        original_model = HouseholdModel(
            id=10,
            owner_user_id=1,
            name="Test Household",
            created_at=now,
        )

        # Act - convert to DTO and back
        dto = HouseholdMapper.to_dto(original_model)
        final_model = HouseholdMapper.to_model(dto)

        # Assert - values should be preserved
        assert final_model.id == original_model.id
        assert final_model.owner_user_id == original_model.owner_user_id
        assert final_model.name == original_model.name
        assert final_model.created_at == original_model.created_at

    def test_to_model_with_special_characters_in_name(self):
        """Test that special characters in name are preserved"""
        # Arrange
        dto = HouseholdDTO(
            household_id=HouseholdID(10),
            owner_user_id=HouseholdUserID(1),
            name=HouseholdName("Smith's Household #1"),
        )

        # Act
        model = HouseholdMapper.to_model(dto)

        # Assert
        assert model.name == "Smith's Household #1"

    def test_to_model_with_max_length_name(self):
        """Test that maximum length name is preserved"""
        # Arrange
        long_name = "H" * 100
        dto = HouseholdDTO(
            household_id=HouseholdID(10),
            owner_user_id=HouseholdUserID(1),
            name=HouseholdName(long_name),
        )

        # Act
        model = HouseholdMapper.to_model(dto)

        # Assert
        assert model.name == long_name
