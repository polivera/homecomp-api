"""Unit tests for HouseholdMemberMapper"""

from datetime import UTC, datetime

import pytest

from app.context.household.domain.dto import HouseholdMemberDTO
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdMemberID,
    HouseholdName,
    HouseholdRole,
    HouseholdUserID,
    HouseholdUserName,
)
from app.context.household.infrastructure.mappers.household_member_mapper import (
    HouseholdMemberMapper,
)
from app.context.household.infrastructure.models import (
    HouseholdMemberModel,
    HouseholdModel,
)
from app.context.user.infrastructure.models import UserModel


@pytest.mark.unit
class TestHouseholdMemberMapper:
    """Tests for HouseholdMemberMapper"""

    def test_to_dto_converts_model_to_dto(self):
        """Test converting database model to domain DTO"""
        # Arrange
        now = datetime.now(UTC)
        model = HouseholdMemberModel(
            id=1,
            household_id=10,
            user_id=2,
            role="participant",
            joined_at=now,
            invited_by_user_id=1,
            invited_at=now,
        )

        # Act
        dto = HouseholdMemberMapper.to_dto(model)

        # Assert
        assert dto is not None
        assert isinstance(dto, HouseholdMemberDTO)
        assert dto.member_id == HouseholdMemberID(1)
        assert dto.household_id == HouseholdID(10)
        assert dto.user_id == HouseholdUserID(2)
        assert dto.role.value == "participant"
        assert dto.joined_at == now
        assert dto.invited_by_user_id == HouseholdUserID(1)
        assert dto.invited_at == now
        assert dto.household_name is None  # Not provided
        assert dto.inviter_username is None  # Not provided

    def test_to_dto_with_household_model(self):
        """Test converting model with household model populated"""
        # Arrange
        now = datetime.now(UTC)
        member_model = HouseholdMemberModel(
            id=1,
            household_id=10,
            user_id=2,
            role="participant",
            joined_at=now,
            invited_by_user_id=1,
            invited_at=now,
        )

        household_model = HouseholdModel(
            id=10,
            owner_user_id=1,
            name="Smith Family",
            created_at=now,
        )

        # Act
        dto = HouseholdMemberMapper.to_dto(member_model, household_model=household_model)

        # Assert
        assert dto.household_name is not None
        assert isinstance(dto.household_name, HouseholdName)
        assert dto.household_name.value == "Smith Family"

    def test_to_dto_with_user_model_username(self):
        """Test converting model with user model (username available)"""
        # Arrange
        now = datetime.now(UTC)
        member_model = HouseholdMemberModel(
            id=1,
            household_id=10,
            user_id=2,
            role="participant",
            joined_at=now,
            invited_by_user_id=1,
            invited_at=now,
        )

        user_model = UserModel(
            id=1,
            email="john@example.com",
            username="john_doe",
            password="hashed_password",
        )

        # Act
        dto = HouseholdMemberMapper.to_dto(member_model, user_model=user_model)

        # Assert
        assert dto.inviter_username is not None
        assert isinstance(dto.inviter_username, HouseholdUserName)
        assert dto.inviter_username.value == "john_doe"

    def test_to_dto_with_user_model_no_username_fallback_to_email(self):
        """Test that email is used when username is None"""
        # Arrange
        now = datetime.now(UTC)
        member_model = HouseholdMemberModel(
            id=1,
            household_id=10,
            user_id=2,
            role="participant",
            joined_at=now,
            invited_by_user_id=1,
            invited_at=now,
        )

        user_model = UserModel(
            id=1,
            email="john@example.com",
            username=None,  # No username
            password="hashed_password",
        )

        # Act
        dto = HouseholdMemberMapper.to_dto(member_model, user_model=user_model)

        # Assert
        assert dto.inviter_username is not None
        assert dto.inviter_username.value == "john@example.com"

    def test_to_dto_pending_invite(self):
        """Test converting model for pending invite (joined_at is None)"""
        # Arrange
        now = datetime.now(UTC)
        model = HouseholdMemberModel(
            id=1,
            household_id=10,
            user_id=2,
            role="participant",
            joined_at=None,  # Pending
            invited_by_user_id=1,
            invited_at=now,
        )

        # Act
        dto = HouseholdMemberMapper.to_dto(model)

        # Assert
        assert dto.joined_at is None
        assert dto.is_invited is True
        assert dto.is_active is False

    def test_to_dto_active_member(self):
        """Test converting model for active member (joined_at is set)"""
        # Arrange
        now = datetime.now(UTC)
        model = HouseholdMemberModel(
            id=1,
            household_id=10,
            user_id=2,
            role="participant",
            joined_at=now,  # Active
            invited_by_user_id=1,
            invited_at=now,
        )

        # Act
        dto = HouseholdMemberMapper.to_dto(model)

        # Assert
        assert dto.joined_at is not None
        assert dto.is_invited is False
        assert dto.is_active is True

    def test_to_dto_with_none_invited_by_user_id(self):
        """Test converting model with None invited_by_user_id"""
        # Arrange
        now = datetime.now(UTC)
        model = HouseholdMemberModel(
            id=1,
            household_id=10,
            user_id=2,
            role="participant",
            joined_at=now,
            invited_by_user_id=None,  # No inviter
            invited_at=now,
        )

        # Act
        dto = HouseholdMemberMapper.to_dto(model)

        # Assert
        assert dto.invited_by_user_id is None

    def test_to_dto_uses_trusted_source_for_role(self):
        """Test that to_dto uses from_trusted_source for role"""
        # Arrange
        now = datetime.now(UTC)
        model = HouseholdMemberModel(
            id=1,
            household_id=10,
            user_id=2,
            role="invalid_role",  # Would fail validation if not using from_trusted_source
            joined_at=now,
            invited_by_user_id=1,
            invited_at=now,
        )

        # Act - should not raise because using from_trusted_source
        dto = HouseholdMemberMapper.to_dto(model)

        # Assert
        assert dto is not None
        assert dto.role.value == "invalid_role"

    def test_to_model_converts_dto_to_model(self):
        """Test converting domain DTO to database model"""
        # Arrange
        now = datetime.now(UTC)
        dto = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=HouseholdID(10),
            user_id=HouseholdUserID(2),
            role=HouseholdRole("participant"),
            joined_at=now,
            invited_by_user_id=HouseholdUserID(1),
            invited_at=now,
        )

        # Act
        model = HouseholdMemberMapper.to_model(dto)

        # Assert
        assert isinstance(model, HouseholdMemberModel)
        assert model.id == 1
        assert model.household_id == 10
        assert model.user_id == 2
        assert model.role == "participant"
        assert model.joined_at == now
        assert model.invited_by_user_id == 1
        assert model.invited_at == now

    def test_to_model_with_none_member_id(self):
        """Test converting DTO without member_id (new entity)"""
        # Arrange
        now = datetime.now(UTC)
        dto = HouseholdMemberDTO(
            member_id=None,  # New member, no ID yet
            household_id=HouseholdID(10),
            user_id=HouseholdUserID(2),
            role=HouseholdRole("participant"),
            joined_at=None,
            invited_by_user_id=HouseholdUserID(1),
            invited_at=now,
        )

        # Act
        model = HouseholdMemberMapper.to_model(dto)

        # Assert
        assert model.id is None  # Will be assigned by database
        assert model.household_id == 10
        assert model.user_id == 2

    def test_to_model_with_none_invited_by_user_id(self):
        """Test converting DTO with None invited_by_user_id"""
        # Arrange
        now = datetime.now(UTC)
        dto = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=HouseholdID(10),
            user_id=HouseholdUserID(2),
            role=HouseholdRole("participant"),
            joined_at=now,
            invited_by_user_id=None,
            invited_at=now,
        )

        # Act
        model = HouseholdMemberMapper.to_model(dto)

        # Assert
        assert model.invited_by_user_id is None

    def test_roundtrip_conversion(self):
        """Test converting model to DTO and back to model"""
        # Arrange
        now = datetime.now(UTC)
        original_model = HouseholdMemberModel(
            id=1,
            household_id=10,
            user_id=2,
            role="participant",
            joined_at=now,
            invited_by_user_id=1,
            invited_at=now,
        )

        # Act - convert to DTO and back
        dto = HouseholdMemberMapper.to_dto(original_model)
        final_model = HouseholdMemberMapper.to_model(dto)

        # Assert - values should be preserved
        assert final_model.id == original_model.id
        assert final_model.household_id == original_model.household_id
        assert final_model.user_id == original_model.user_id
        assert final_model.role == original_model.role
        assert final_model.joined_at == original_model.joined_at
        assert final_model.invited_by_user_id == original_model.invited_by_user_id
        assert final_model.invited_at == original_model.invited_at

    def test_to_dto_or_fail_with_valid_model(self):
        """Test to_dto_or_fail with valid model"""
        # Arrange
        now = datetime.now(UTC)
        model = HouseholdMemberModel(
            id=1,
            household_id=10,
            user_id=2,
            role="participant",
            joined_at=now,
            invited_by_user_id=1,
            invited_at=now,
        )

        # Act
        dto = HouseholdMemberMapper.to_dto_or_fail(model)

        # Assert
        assert dto is not None
        assert isinstance(dto, HouseholdMemberDTO)
