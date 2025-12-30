from datetime import UTC, datetime
from typing import Any, cast

from sqlalchemy import and_, select, union, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.context.household.domain.contracts import HouseholdRepositoryContract
from app.context.household.domain.dto import HouseholdDTO, HouseholdMemberDTO
from app.context.household.domain.exceptions import (
    HouseholdNameAlreadyExistError,
    HouseholdNotFoundError,
    InviteNotFoundError,
)
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdName,
    HouseholdUserID,
)
from app.context.household.infrastructure.mappers import (
    HouseholdMapper,
    HouseholdMemberMapper,
)
from app.context.household.infrastructure.models import (
    HouseholdMemberModel,
    HouseholdModel,
)
from app.context.user.infrastructure.models.user_model import UserModel


class HouseholdRepository(HouseholdRepositoryContract):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create_household(self, household_dto: HouseholdDTO) -> HouseholdDTO:
        """Create a new household with the owner stored in the household table"""

        household_model = HouseholdMapper.to_model(household_dto)

        self._db.add(household_model)

        try:
            await self._db.commit()
            await self._db.refresh(household_model)
        except IntegrityError as e:
            await self._db.rollback()
            if "uq_households_owner_name" in str(e.orig):
                raise HouseholdNameAlreadyExistError(
                    f"Household with name '{household_dto.name.value}' already exists for this user"
                ) from None
            raise Exception(e) from None

        return HouseholdMapper.to_dto_or_fail(household_model)

    async def find_household_by_name(self, name: HouseholdName, user_id: HouseholdUserID) -> HouseholdDTO | None:
        """Find a household by name for a specific user (owner)"""

        stmt = select(HouseholdModel).where(
            and_(
                HouseholdModel.owner_user_id == user_id.value,
                HouseholdModel.name == name.value,
                HouseholdModel.deleted_at.is_(None),
            )
        )

        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()

        return HouseholdMapper.to_dto(model) if model else None

    async def find_household_by_id(self, household_id: HouseholdID) -> HouseholdDTO | None:
        """Find a household by ID"""

        stmt = select(HouseholdModel).where(
            and_(
                HouseholdModel.id == household_id.value,
                HouseholdModel.deleted_at.is_(None),
            )
        )

        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()

        return HouseholdMapper.to_dto(model) if model else None

    # Member management methods
    async def create_member(self, member: HouseholdMemberDTO) -> HouseholdMemberDTO:
        """Create a new household member (for invites or direct adds)"""
        member_model = HouseholdMemberMapper.to_model(member)
        self._db.add(member_model)

        await self._db.commit()
        await self._db.refresh(member_model)

        return HouseholdMemberMapper.to_dto_or_fail(member_model)

    async def find_member(self, household_id: HouseholdID, user_id: HouseholdUserID) -> HouseholdMemberDTO | None:
        """Find the most recent member record for user in household"""
        stmt = (
            select(HouseholdMemberModel)
            .where(
                and_(
                    HouseholdMemberModel.household_id == household_id.value,
                    HouseholdMemberModel.user_id == user_id.value,
                )
            )
            .order_by(HouseholdMemberModel.invited_at.desc())
            .limit(1)
        )

        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()

        return HouseholdMemberMapper.to_dto(model) if model else None

    async def accept_invite(self, household_id: HouseholdID, user_id: HouseholdUserID) -> HouseholdMemberDTO:
        """Accept invite by setting joined_at to current timestamp"""
        # Find the pending invite
        stmt = (
            select(HouseholdMemberModel)
            .where(
                and_(
                    HouseholdMemberModel.household_id == household_id.value,
                    HouseholdMemberModel.user_id == user_id.value,
                    HouseholdMemberModel.joined_at.is_(None),
                )
            )
            .order_by(HouseholdMemberModel.invited_at.desc())
            .limit(1)
        )

        result = await self._db.execute(stmt)
        member_model = result.scalar_one_or_none()

        if not member_model:
            raise InviteNotFoundError("No pending invite found")

        # Update joined_at
        member_model.joined_at = datetime.now(UTC)

        await self._db.commit()
        await self._db.refresh(member_model)

        return HouseholdMemberMapper.to_dto_or_fail(member_model)

    async def revoke_or_remove(self, household_id: HouseholdID, user_id: HouseholdUserID) -> None:
        """Revoke invite or remove member by setting left_at to current timestamp"""
        # Find active invite or membership
        stmt = (
            select(HouseholdMemberModel)
            .where(
                and_(
                    HouseholdMemberModel.household_id == household_id.value,
                    HouseholdMemberModel.user_id == user_id.value,
                )
            )
            .order_by(HouseholdMemberModel.invited_at.desc())
            .limit(1)
        )

        result = await self._db.execute(stmt)
        member_model = result.scalar_one_or_none()

        if not member_model:
            raise InviteNotFoundError("No active invite or membership found")

        await self._db.commit()

    async def list_user_households(self, user_id: HouseholdUserID) -> list[HouseholdDTO]:
        """List all households user owns or is an active participant in"""
        # Get households where user is owner
        owner_stmt = select(HouseholdModel).where(
            and_(
                HouseholdModel.owner_user_id == user_id.value,
                HouseholdModel.deleted_at.is_(None),
            )
        )

        # Get households where user is active member
        member_stmt = (
            select(HouseholdModel)
            .join(
                HouseholdMemberModel,
                HouseholdModel.id == HouseholdMemberModel.household_id,
            )
            .where(
                and_(
                    HouseholdMemberModel.user_id == user_id.value,
                    HouseholdMemberModel.joined_at.isnot(None),
                    HouseholdModel.deleted_at.is_(None),
                )
            )
        )

        # Combine with UNION (automatically deduplicates)
        combined_stmt = union(owner_stmt, member_stmt)

        result = await self._db.execute(combined_stmt)
        households = result.scalars().all()

        return [HouseholdMapper.to_dto_or_fail(h) for h in households]

    async def list_user_pending_invites(self, user_id: HouseholdUserID) -> list[HouseholdDTO]:
        """List all households user has been invited to but not yet accepted"""
        stmt = (
            select(HouseholdModel)
            .join(
                HouseholdMemberModel,
                HouseholdModel.id == HouseholdMemberModel.household_id,
            )
            .where(
                and_(
                    HouseholdMemberModel.user_id == user_id.value,
                    HouseholdMemberModel.joined_at.is_(None),
                    HouseholdModel.deleted_at.is_(None),
                )
            )
        )

        result = await self._db.execute(stmt)
        households = result.scalars().all()

        return [HouseholdMapper.to_dto_or_fail(h) for h in households]

    async def list_user_pending_household_invites(self, user_id: HouseholdUserID) -> list[HouseholdMemberDTO]:
        """List user pending invitation to households"""
        InviterUser = aliased(UserModel)
        stmt = (
            select(HouseholdMemberModel, HouseholdModel, InviterUser)
            .join(HouseholdModel, HouseholdModel.id == HouseholdMemberModel.household_id)
            .join(InviterUser, InviterUser.id == HouseholdMemberModel.invited_by_user_id)
            .where(
                and_(
                    HouseholdMemberModel.user_id == user_id.value,
                    HouseholdMemberModel.joined_at.is_(None),
                    HouseholdModel.deleted_at.is_(None),
                )
            )
        )

        result = await self._db.execute(stmt)
        rows = result.all()

        # Each row is a tuple: (HouseholdMemberModel, HouseholdModel, InviterUser)
        member_list = []
        for member_model, household_model, inviter_model in rows:
            member_dto = HouseholdMemberMapper.to_dto(member_model, household_model, inviter_model)
            member_list.append(member_dto)

        return member_list

    async def list_household_pending_invites(
        self, household_id: HouseholdID, owner_id: HouseholdUserID
    ) -> list[HouseholdMemberDTO]:
        """List all pending invites for a household with household name and inviter username"""
        # Create alias for the inviter user
        InviterUser = aliased(UserModel)

        # Join with HouseholdModel and UserModel to get household name and inviter username
        stmt = (
            select(HouseholdMemberModel, HouseholdModel, InviterUser)
            .join(HouseholdModel, HouseholdModel.id == HouseholdMemberModel.household_id)
            .join(InviterUser, InviterUser.id == HouseholdMemberModel.invited_by_user_id)
            .where(
                and_(
                    HouseholdMemberModel.household_id == household_id.value,
                    HouseholdModel.owner_user_id == owner_id.value,
                    HouseholdMemberModel.joined_at.is_(None),
                    HouseholdModel.deleted_at.is_(None),
                )
            )
        )

        result = await self._db.execute(stmt)
        rows = result.all()

        # Each row is a tuple: (HouseholdMemberModel, HouseholdModel, InviterUser)
        member_list = []
        for member_model, household_model, inviter_model in rows:
            member_dto = HouseholdMemberMapper.to_dto(member_model, household_model, inviter_model)
            member_list.append(member_dto)

        return member_list

    async def update_household(self, household: HouseholdDTO) -> HouseholdDTO:
        """Update household name"""
        if household.household_id is None:
            raise ValueError("Household ID not given")

        stmt = (
            update(HouseholdModel)
            .where(
                and_(
                    HouseholdModel.id == household.household_id.value,
                    HouseholdModel.deleted_at.is_(None),
                )
            )
            .values(name=household.name.value)
        )

        result = cast(CursorResult[Any], await self._db.execute(stmt))
        if result.rowcount == 0:
            raise HouseholdNotFoundError(
                f"Household with ID {household.household_id.value} not found or already deleted"
            )

        await self._db.commit()
        return household

    async def delete_household(self, household_id: HouseholdID, user_id: HouseholdUserID) -> bool:
        """Soft delete a household (owner only)"""
        # Verify exists and user owns it
        household = await self.find_household_by_id(household_id)
        # if not household or household.owner_user_id.value != user_id.value:
        if not household or not household.owner_user_id.is_equal(user_id):
            return False

        # Soft delete
        stmt = (
            update(HouseholdModel)
            .where(
                and_(
                    HouseholdModel.id == household_id.value,
                    HouseholdModel.owner_user_id == user_id.value,
                    HouseholdModel.deleted_at.is_(None),
                )
            )
            .values(deleted_at=datetime.now(UTC))
        )

        result = cast(CursorResult[Any], await self._db.execute(stmt))
        await self._db.commit()

        return result.rowcount > 0

    async def user_has_access(self, user_id: HouseholdUserID, household_id: HouseholdID) -> bool:
        """Check if user owns or is an active member of household"""
        # Check if owner
        household = await self.find_household_by_id(household_id)
        if household and household.owner_user_id.value == user_id.value:
            return True

        # Check if active member
        member = await self.find_member(household_id, user_id)
        if member and member.is_active:
            return True

        return False
