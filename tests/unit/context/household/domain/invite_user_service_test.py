"""Unit tests for InviteUserService"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.household.domain.dto import HouseholdDTO, HouseholdMemberDTO
from app.context.household.domain.exceptions import (
    AlreadyActiveMemberError,
    AlreadyInvitedError,
    OnlyOwnerCanInviteError,
)
from app.context.household.domain.services.invite_user_service import InviteUserService
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdMemberID,
    HouseholdName,
    HouseholdRole,
    HouseholdUserID,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestInviteUserService:
    """Tests for InviteUserService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository, mock_logger):
        """Create service with mocked repository and logger"""
        return InviteUserService(mock_repository, mock_logger)

    @pytest.mark.asyncio
    async def test_invite_user_success(self, service, mock_repository):
        """Test successful user invitation"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        invitee_id = HouseholdUserID(2)
        role = HouseholdRole("participant")

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        expected_member_dto = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=invitee_id,
            role=role,
            joined_at=None,  # Pending invite
            invited_by_user_id=owner_id,
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=None)  # Not a member yet
        mock_repository.create_member = AsyncMock(return_value=expected_member_dto)

        # Act
        result = await service.invite_user(
            inviter_user_id=owner_id,
            household_id=household_id,
            invitee_user_id=invitee_id,
            role=role,
        )

        # Assert
        assert result == expected_member_dto
        assert result.is_invited is True
        assert result.is_active is False
        mock_repository.find_household_by_id.assert_called_once_with(household_id)
        mock_repository.find_member.assert_called_once_with(household_id, invitee_id)
        mock_repository.create_member.assert_called_once()

    @pytest.mark.asyncio
    async def test_invite_user_non_owner_raises_error(self, service, mock_repository):
        """Test that non-owner cannot invite users"""
        # Arrange
        owner_id = HouseholdUserID(1)
        non_owner_id = HouseholdUserID(99)
        household_id = HouseholdID(10)
        invitee_id = HouseholdUserID(2)
        role = HouseholdRole("participant")

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,  # Actual owner
            name=HouseholdName("Smith Family"),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)

        # Act & Assert
        with pytest.raises(OnlyOwnerCanInviteError, match="Only the household owner can invite users"):
            await service.invite_user(
                inviter_user_id=non_owner_id,  # Not the owner
                household_id=household_id,
                invitee_user_id=invitee_id,
                role=role,
            )

    @pytest.mark.asyncio
    async def test_invite_user_household_not_found_raises_error(self, service, mock_repository):
        """Test that non-existent household raises error"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(999)
        invitee_id = HouseholdUserID(2)
        role = HouseholdRole("participant")

        mock_repository.find_household_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(OnlyOwnerCanInviteError, match="Only the household owner can invite users"):
            await service.invite_user(
                inviter_user_id=owner_id,
                household_id=household_id,
                invitee_user_id=invitee_id,
                role=role,
            )

    @pytest.mark.asyncio
    async def test_invite_user_already_active_raises_error(self, service, mock_repository):
        """Test that inviting an already active member raises error"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        invitee_id = HouseholdUserID(2)
        role = HouseholdRole("participant")

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        # Existing active member
        existing_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=invitee_id,
            role=role,
            joined_at=datetime.now(UTC),  # Active (has joined_at)
            invited_by_user_id=owner_id,
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=existing_member)

        # Act & Assert
        with pytest.raises(
            AlreadyActiveMemberError,
            match="User is already an active member of this household",
        ):
            await service.invite_user(
                inviter_user_id=owner_id,
                household_id=household_id,
                invitee_user_id=invitee_id,
                role=role,
            )

    @pytest.mark.asyncio
    async def test_invite_user_already_invited_raises_error(self, service, mock_repository):
        """Test that inviting an already invited user raises error"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        invitee_id = HouseholdUserID(2)
        role = HouseholdRole("participant")

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        # Existing pending invite
        existing_member = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=invitee_id,
            role=role,
            joined_at=None,  # Pending invite
            invited_by_user_id=owner_id,
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=existing_member)

        # Act & Assert
        with pytest.raises(
            AlreadyInvitedError,
            match="User already has a pending invite to this household",
        ):
            await service.invite_user(
                inviter_user_id=owner_id,
                household_id=household_id,
                invitee_user_id=invitee_id,
                role=role,
            )

    @pytest.mark.asyncio
    async def test_invite_user_creates_member_with_correct_data(self, service, mock_repository):
        """Test that invite creates member DTO with correct structure"""
        # Arrange
        owner_id = HouseholdUserID(1)
        household_id = HouseholdID(10)
        invitee_id = HouseholdUserID(2)
        role = HouseholdRole("participant")

        household_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=owner_id,
            name=HouseholdName("Smith Family"),
        )

        expected_member_dto = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=household_id,
            user_id=invitee_id,
            role=role,
            joined_at=None,
            invited_by_user_id=owner_id,
            invited_at=datetime.now(UTC),
        )

        mock_repository.find_household_by_id = AsyncMock(return_value=household_dto)
        mock_repository.find_member = AsyncMock(return_value=None)
        mock_repository.create_member = AsyncMock(return_value=expected_member_dto)

        # Act
        await service.invite_user(
            inviter_user_id=owner_id,
            household_id=household_id,
            invitee_user_id=invitee_id,
            role=role,
        )

        # Assert - verify the DTO passed to create_member
        call_args = mock_repository.create_member.call_args[0][0]
        assert call_args.member_id is None  # New member, no ID yet
        assert call_args.household_id == household_id
        assert call_args.user_id == invitee_id
        assert call_args.role == role
        assert call_args.joined_at is None  # Pending invite
        assert call_args.invited_by_user_id == owner_id
        assert call_args.invited_at is not None
