"""Unit tests for DeclineInviteService"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.household.domain.dto import HouseholdMemberDTO
from app.context.household.domain.exceptions import NotInvitedError
from app.context.household.domain.services.decline_invite_service import (
    DeclineInviteService,
)
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdMemberID,
    HouseholdRole,
    HouseholdUserID,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestDeclineInviteService:
    """Tests for DeclineInviteService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository):
        """Create service with mocked repository"""
        return DeclineInviteService(mock_repository)

    @pytest.mark.asyncio
    async def test_decline_invite_success(self, service, mock_repository):
        """Test successful invite decline"""
        # Arrange
        user_id = HouseholdUserID(2)
        household_id = HouseholdID(10)

        # Pending invite
        pending_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=user_id,
            role=HouseholdRole("participant"),
            joined_at=None,  # Pending
            invited_by_user_id=HouseholdUserID(1),
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_member = AsyncMock(return_value=pending_member)
        mock_repository.revoke_or_remove = AsyncMock(return_value=None)

        # Act
        result = await service.decline_invite(user_id=user_id, household_id=household_id)

        # Assert
        assert result is None
        mock_repository.find_member.assert_called_once_with(household_id, user_id)
        mock_repository.revoke_or_remove.assert_called_once_with(household_id, user_id)

    @pytest.mark.asyncio
    async def test_decline_invite_no_invite_raises_error(self, service, mock_repository):
        """Test that declining without invite raises NotInvitedError"""
        # Arrange
        user_id = HouseholdUserID(2)
        household_id = HouseholdID(10)

        mock_repository.find_member = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(NotInvitedError, match="No pending invite found for this household"):
            await service.decline_invite(user_id=user_id, household_id=household_id)

    @pytest.mark.asyncio
    async def test_decline_invite_already_active_raises_error(self, service, mock_repository):
        """Test that declining when already active raises error"""
        # Arrange
        user_id = HouseholdUserID(2)
        household_id = HouseholdID(10)

        # Already active member
        active_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=user_id,
            role=HouseholdRole("participant"),
            joined_at=datetime.now(UTC),  # Already active
            invited_by_user_id=HouseholdUserID(1),
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_member = AsyncMock(return_value=active_member)

        # Act & Assert
        with pytest.raises(NotInvitedError, match="No pending invite found for this household"):
            await service.decline_invite(user_id=user_id, household_id=household_id)

    @pytest.mark.asyncio
    async def test_decline_invite_propagates_repository_exceptions(self, service, mock_repository):
        """Test that repository exceptions are propagated"""
        # Arrange
        user_id = HouseholdUserID(2)
        household_id = HouseholdID(10)

        pending_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=user_id,
            role=HouseholdRole("participant"),
            joined_at=None,
            invited_by_user_id=HouseholdUserID(1),
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_member = AsyncMock(return_value=pending_member)
        mock_repository.revoke_or_remove = AsyncMock(side_effect=Exception("Database error"))

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await service.decline_invite(user_id=user_id, household_id=household_id)
