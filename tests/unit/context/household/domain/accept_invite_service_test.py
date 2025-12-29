"""Unit tests for AcceptInviteService"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.household.domain.dto import HouseholdMemberDTO
from app.context.household.domain.exceptions import NotInvitedError
from app.context.household.domain.services.accept_invite_service import (
    AcceptInviteService,
)
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdMemberID,
    HouseholdRole,
    HouseholdUserID,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestAcceptInviteService:
    """Tests for AcceptInviteService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository):
        """Create service with mocked repository"""
        return AcceptInviteService(mock_repository)

    @pytest.mark.asyncio
    async def test_accept_invite_success(self, service, mock_repository):
        """Test successful invite acceptance"""
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

        # Accepted member (with joined_at set)
        accepted_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=user_id,
            role=HouseholdRole("participant"),
            joined_at=datetime.now(UTC),  # Accepted
            invited_by_user_id=HouseholdUserID(1),
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_member = AsyncMock(return_value=pending_member)
        mock_repository.accept_invite = AsyncMock(return_value=accepted_member)

        # Act
        result = await service.accept_invite(user_id=user_id, household_id=household_id)

        # Assert
        assert result == accepted_member
        assert result.is_active is True
        assert result.is_invited is False
        mock_repository.find_member.assert_called_once_with(household_id, user_id)
        mock_repository.accept_invite.assert_called_once_with(household_id, user_id)

    @pytest.mark.asyncio
    async def test_accept_invite_no_invite_raises_error(self, service, mock_repository):
        """Test that accepting without invite raises NotInvitedError"""
        # Arrange
        user_id = HouseholdUserID(2)
        household_id = HouseholdID(10)

        mock_repository.find_member = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(
            NotInvitedError, match="No pending invite found for this household"
        ):
            await service.accept_invite(user_id=user_id, household_id=household_id)

    @pytest.mark.asyncio
    async def test_accept_invite_already_active_raises_error(
        self, service, mock_repository
    ):
        """Test that accepting when already active raises error"""
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
        with pytest.raises(
            NotInvitedError, match="No pending invite found for this household"
        ):
            await service.accept_invite(user_id=user_id, household_id=household_id)

    @pytest.mark.asyncio
    async def test_accept_invite_propagates_repository_exceptions(
        self, service, mock_repository
    ):
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
        mock_repository.accept_invite = AsyncMock(side_effect=Exception("Database error"))

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await service.accept_invite(user_id=user_id, household_id=household_id)
