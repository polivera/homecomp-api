"""Unit tests for RevokeInviteService"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.household.domain.dto import HouseholdDTO, HouseholdMemberDTO
from app.context.household.domain.exceptions import (
    InviteNotFoundError,
    OnlyOwnerCanRevokeError,
)
from app.context.household.domain.services.revoke_invite_service import (
    RevokeInviteService,
)
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdMemberID,
    HouseholdName,
    HouseholdRole,
    HouseholdUserID,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestRevokeInviteService:
    """Tests for RevokeInviteService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository, mock_logger):
        """Create service with mocked repository and logger"""
        return RevokeInviteService(mock_repository, mock_logger)

    @pytest.mark.asyncio
    async def test_revoke_invite_success(self, service, mock_repository):
        """Test successful invite revocation"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        invitee_id = HouseholdUserID(2)

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        # Pending invite
        pending_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=invitee_id,
            role=HouseholdRole("participant"),
            joined_at=None,  # Pending
            invited_by_user_id=owner_id,
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=pending_member)
        mock_repository.revoke_or_remove = AsyncMock(return_value=None)

        # Act
        result = await service.revoke_invite(
            revoker_user_id=owner_id,
            household_id=household_id,
            invitee_user_id=invitee_id,
        )

        # Assert
        assert result is None
        mock_repository.find_household_by_id.assert_called_once_with(household_id)
        mock_repository.find_member.assert_called_once_with(household_id, invitee_id)
        mock_repository.revoke_or_remove.assert_called_once_with(household_id, invitee_id)

    @pytest.mark.asyncio
    async def test_revoke_invite_non_owner_raises_error(self, service, mock_repository):
        """Test that non-owner cannot revoke invites"""
        # Arrange
        owner_id = HouseholdUserID(1)
        non_owner_id = HouseholdUserID(99)
        household_id = HouseholdID(10)
        invitee_id = HouseholdUserID(2)

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,  # Actual owner
            name=HouseholdName("Smith Family"),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)

        # Act & Assert
        with pytest.raises(
            OnlyOwnerCanRevokeError,
            match="Only the household owner can revoke invites",
        ):
            await service.revoke_invite(
                revoker_user_id=non_owner_id,  # Not the owner
                household_id=household_id,
                invitee_user_id=invitee_id,
            )

    @pytest.mark.asyncio
    async def test_revoke_invite_household_not_found_raises_error(self, service, mock_repository):
        """Test that non-existent household raises error"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(999)
        invitee_id = HouseholdUserID(2)

        mock_repository.find_household_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(
            OnlyOwnerCanRevokeError,
            match="Only the household owner can revoke invites",
        ):
            await service.revoke_invite(
                revoker_user_id=owner_id,
                household_id=household_id,
                invitee_user_id=invitee_id,
            )

    @pytest.mark.asyncio
    async def test_revoke_invite_not_found_raises_error(self, service, mock_repository):
        """Test that revoking non-existent invite raises error"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        invitee_id = HouseholdUserID(999)

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(InviteNotFoundError, match="No pending invite found for this user"):
            await service.revoke_invite(
                revoker_user_id=owner_id,
                household_id=household_id,
                invitee_user_id=invitee_id,
            )

    @pytest.mark.asyncio
    async def test_revoke_invite_already_active_raises_error(self, service, mock_repository):
        """Test that revoking active member (not invite) raises error"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        invitee_id = HouseholdUserID(2)

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        # Active member (not pending)
        active_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=invitee_id,
            role=HouseholdRole("participant"),
            joined_at=datetime.now(UTC),  # Active
            invited_by_user_id=owner_id,
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=active_member)

        # Act & Assert
        with pytest.raises(InviteNotFoundError, match="No pending invite found for this user"):
            await service.revoke_invite(
                revoker_user_id=owner_id,
                household_id=household_id,
                invitee_user_id=invitee_id,
            )

    @pytest.mark.asyncio
    async def test_revoke_invite_propagates_repository_exceptions(self, service, mock_repository):
        """Test that repository exceptions are propagated"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        invitee_id = HouseholdUserID(2)

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        pending_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=invitee_id,
            role=HouseholdRole("participant"),
            joined_at=None,
            invited_by_user_id=owner_id,
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=pending_member)
        mock_repository.revoke_or_remove = AsyncMock(side_effect=Exception("Database error"))

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await service.revoke_invite(
                revoker_user_id=owner_id,
                household_id=household_id,
                invitee_user_id=invitee_id,
            )
