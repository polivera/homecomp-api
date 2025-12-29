"""Unit tests for InviteUserHandler"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.household.application.commands import InviteUserCommand
from app.context.household.application.dto import InviteUserErrorCode
from app.context.household.application.handlers.invite_user_handler import (
    InviteUserHandler,
)
from app.context.household.domain.dto import HouseholdMemberDTO
from app.context.household.domain.exceptions import (
    AlreadyActiveMemberError,
    AlreadyInvitedError,
    HouseholdMapperError,
    OnlyOwnerCanInviteError,
)
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdMemberID,
    HouseholdRole,
    HouseholdUserID,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestInviteUserHandler:
    """Tests for InviteUserHandler"""

    @pytest.fixture
    def mock_service(self):
        """Create a mock service"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_service):
        """Create handler with mocked service"""
        return InviteUserHandler(mock_service)

    @pytest.mark.asyncio
    async def test_invite_user_success(self, handler, mock_service):
        """Test successful user invitation"""
        # Arrange
        command = InviteUserCommand(inviter_user_id=1, household_id=10, invitee_user_id=2, role="participant")

        member_dto = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=HouseholdID(10),
            user_id=HouseholdUserID(2),
            role=HouseholdRole("participant"),
            joined_at=None,
            invited_by_user_id=HouseholdUserID(1),
            invited_at=datetime.now(UTC),
        )

        mock_service.invite_user = AsyncMock(return_value=member_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.member_id == 1
        assert result.household_id == 10
        assert result.user_id == 2
        assert result.role == "participant"
        mock_service.invite_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_invite_user_without_member_id_returns_error(self, handler, mock_service):
        """Test that missing member_id in result returns error"""
        # Arrange
        command = InviteUserCommand(inviter_user_id=1, household_id=10, invitee_user_id=2, role="participant")

        member_dto = HouseholdMemberDTO(
            member_id=None,  # Missing ID
            household_id=HouseholdID(10),
            user_id=HouseholdUserID(2),
            role=HouseholdRole("participant"),
            joined_at=None,
            invited_by_user_id=HouseholdUserID(1),
            invited_at=datetime.now(UTC),
        )

        mock_service.invite_user = AsyncMock(return_value=member_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == InviteUserErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Error creating invitation"
        assert result.member_id is None

    @pytest.mark.asyncio
    async def test_invite_user_only_owner_can_invite_error(self, handler, mock_service):
        """Test handling of non-owner attempting to invite"""
        # Arrange
        command = InviteUserCommand(inviter_user_id=99, household_id=10, invitee_user_id=2, role="participant")

        mock_service.invite_user = AsyncMock(side_effect=OnlyOwnerCanInviteError("Only owner can invite"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == InviteUserErrorCode.ONLY_OWNER_CAN_INVITE
        assert result.error_message == "Only the household owner can invite users"
        assert result.member_id is None

    @pytest.mark.asyncio
    async def test_invite_user_already_active_member_error(self, handler, mock_service):
        """Test handling of already active member exception"""
        # Arrange
        command = InviteUserCommand(inviter_user_id=1, household_id=10, invitee_user_id=2, role="participant")

        mock_service.invite_user = AsyncMock(side_effect=AlreadyActiveMemberError("Already active"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == InviteUserErrorCode.ALREADY_ACTIVE_MEMBER
        assert result.error_message == "User is already an active member of this household"
        assert result.member_id is None

    @pytest.mark.asyncio
    async def test_invite_user_already_invited_error(self, handler, mock_service):
        """Test handling of already invited exception"""
        # Arrange
        command = InviteUserCommand(inviter_user_id=1, household_id=10, invitee_user_id=2, role="participant")

        mock_service.invite_user = AsyncMock(side_effect=AlreadyInvitedError("Already invited"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == InviteUserErrorCode.ALREADY_INVITED
        assert result.error_message == "User already has a pending invite to this household"
        assert result.member_id is None

    @pytest.mark.asyncio
    async def test_invite_user_mapper_error(self, handler, mock_service):
        """Test handling of mapper exception"""
        # Arrange
        command = InviteUserCommand(inviter_user_id=1, household_id=10, invitee_user_id=2, role="participant")

        mock_service.invite_user = AsyncMock(side_effect=HouseholdMapperError("Mapping failed"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == InviteUserErrorCode.MAPPER_ERROR
        assert result.error_message == "Error mapping model to DTO"
        assert result.member_id is None

    @pytest.mark.asyncio
    async def test_invite_user_unexpected_error(self, handler, mock_service):
        """Test handling of unexpected exception"""
        # Arrange
        command = InviteUserCommand(inviter_user_id=1, household_id=10, invitee_user_id=2, role="participant")

        mock_service.invite_user = AsyncMock(side_effect=Exception("Database error"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == InviteUserErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Unexpected error"
        assert result.member_id is None

    @pytest.mark.asyncio
    async def test_invite_user_converts_primitives_to_value_objects(self, handler, mock_service):
        """Test that handler converts command primitives to value objects"""
        # Arrange
        command = InviteUserCommand(inviter_user_id=1, household_id=10, invitee_user_id=2, role="participant")

        member_dto = HouseholdMemberDTO(
            member_id=HouseholdMemberID(1),
            household_id=HouseholdID(10),
            user_id=HouseholdUserID(2),
            role=HouseholdRole("participant"),
            joined_at=None,
            invited_by_user_id=HouseholdUserID(1),
            invited_at=datetime.now(UTC),
        )

        mock_service.invite_user = AsyncMock(return_value=member_dto)

        # Act
        await handler.handle(command)

        # Assert - verify service was called with value objects
        call_args = mock_service.invite_user.call_args
        assert isinstance(call_args.kwargs["inviter_user_id"], HouseholdUserID)
        assert isinstance(call_args.kwargs["household_id"], HouseholdID)
        assert isinstance(call_args.kwargs["invitee_user_id"], HouseholdUserID)
        assert isinstance(call_args.kwargs["role"], HouseholdRole)
