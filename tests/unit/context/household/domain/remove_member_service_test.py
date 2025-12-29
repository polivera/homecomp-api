"""Unit tests for RemoveMemberService"""

import pytest
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

from app.context.household.domain.services.remove_member_service import (
    RemoveMemberService,
)
from app.context.household.domain.dto import HouseholdDTO, HouseholdMemberDTO
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdMemberID,
    HouseholdName,
    HouseholdRole,
    HouseholdUserID,
)
from app.context.household.domain.exceptions import (
    CannotRemoveSelfError,
    InviteNotFoundError,
    OnlyOwnerCanRemoveMemberError,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestRemoveMemberService:
    """Tests for RemoveMemberService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository):
        """Create service with mocked repository"""
        return RemoveMemberService(mock_repository)

    @pytest.mark.asyncio
    async def test_remove_member_success(self, service, mock_repository):
        """Test successful member removal"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        member_id = HouseholdUserID(2)

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        # Active member
        active_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=member_id,
            role=HouseholdRole("participant"),
            joined_at=datetime.now(UTC),  # Active
            invited_by_user_id=owner_id,
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=active_member)
        mock_repository.revoke_or_remove = AsyncMock(return_value=None)

        # Act
        result = await service.remove_member(
            remover_user_id=owner_id,
            household_id=household_id,
            member_user_id=member_id,
        )

        # Assert
        assert result is None
        mock_repository.find_household_by_id.assert_called_once_with(household_id)
        mock_repository.find_member.assert_called_once_with(household_id, member_id)
        mock_repository.revoke_or_remove.assert_called_once_with(household_id, member_id)

    @pytest.mark.asyncio
    async def test_remove_member_non_owner_raises_error(self, service, mock_repository):
        """Test that non-owner cannot remove members"""
        # Arrange
        owner_id = HouseholdUserID(1)
        non_owner_id = HouseholdUserID(99)
        household_id = HouseholdID(10)
        member_id = HouseholdUserID(2)

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,  # Actual owner
            name=HouseholdName("Smith Family"),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)

        # Act & Assert
        with pytest.raises(
            OnlyOwnerCanRemoveMemberError,
            match="Only the household owner can remove members",
        ):
            await service.remove_member(
                remover_user_id=non_owner_id,  # Not the owner
                household_id=household_id,
                member_user_id=member_id,
            )

    @pytest.mark.asyncio
    async def test_remove_member_household_not_found_raises_error(
        self, service, mock_repository
    ):
        """Test that non-existent household raises error"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(999)
        member_id = HouseholdUserID(2)

        mock_repository.find_household_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(
            OnlyOwnerCanRemoveMemberError,
            match="Only the household owner can remove members",
        ):
            await service.remove_member(
                remover_user_id=owner_id,
                household_id=household_id,
                member_user_id=member_id,
            )

    @pytest.mark.asyncio
    async def test_remove_member_cannot_remove_self_raises_error(
        self, service, mock_repository
    ):
        """Test that owner cannot remove themselves"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)

        # Act & Assert
        with pytest.raises(
            CannotRemoveSelfError,
            match="Owner cannot remove themselves from the household",
        ):
            await service.remove_member(
                remover_user_id=owner_id,
                household_id=household_id,
                member_user_id=owner_id,  # Same as owner
            )

    @pytest.mark.asyncio
    async def test_remove_member_not_found_raises_error(self, service, mock_repository):
        """Test that removing non-existent member raises error"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        member_id = HouseholdUserID(999)

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(
            InviteNotFoundError, match="No active member found with this user ID"
        ):
            await service.remove_member(
                remover_user_id=owner_id,
                household_id=household_id,
                member_user_id=member_id,
            )

    @pytest.mark.asyncio
    async def test_remove_member_not_active_raises_error(self, service, mock_repository):
        """Test that removing pending invite (not active) raises error"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        member_id = HouseholdUserID(2)

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        # Pending member (not active)
        pending_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=member_id,
            role=HouseholdRole("participant"),
            joined_at=None,  # Not active
            invited_by_user_id=owner_id,
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=pending_member)

        # Act & Assert
        with pytest.raises(
            InviteNotFoundError, match="No active member found with this user ID"
        ):
            await service.remove_member(
                remover_user_id=owner_id,
                household_id=household_id,
                member_user_id=member_id,
            )

    @pytest.mark.asyncio
    async def test_remove_member_propagates_repository_exceptions(
        self, service, mock_repository
    ):
        """Test that repository exceptions are propagated"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        member_id = HouseholdUserID(2)

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        active_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=member_id,
            role=HouseholdRole("participant"),
            joined_at=datetime.now(UTC),
            invited_by_user_id=owner_id,
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=active_member)
        mock_repository.revoke_or_remove = AsyncMock(
            side_effect=Exception("Database error")
        )

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await service.remove_member(
                remover_user_id=owner_id,
                household_id=household_id,
                member_user_id=member_id,
            )
