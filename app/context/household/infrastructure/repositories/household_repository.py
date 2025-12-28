from datetime import UTC, datetime
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.household.domain.contracts import HouseholdRepositoryContract
from app.context.household.domain.dto import HouseholdDTO, HouseholdMemberDTO
from app.context.household.domain.exceptions import (
    HouseholdNameAlreadyExistError,
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


class HouseholdRepository(HouseholdRepositoryContract):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create_household(
        self, household_dto: HouseholdDTO, creator_user_id: HouseholdUserID
    ) -> HouseholdDTO:
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
                )
            raise Exception(e)

        return HouseholdMapper.to_dto_or_fail(household_model)

    async def find_household_by_name(
        self, name: HouseholdName, user_id: HouseholdUserID
    ) -> Optional[HouseholdDTO]:
        """Find a household by name for a specific user (owner)"""

        stmt = select(HouseholdModel).where(
            and_(
                HouseholdModel.owner_user_id == user_id.value,
                HouseholdModel.name == name.value,
            )
        )

        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()

        return HouseholdMapper.to_dto(model) if model else None

    async def find_household_by_id(
        self, household_id: HouseholdID
    ) -> Optional[HouseholdDTO]:
        """Find a household by ID"""

        stmt = select(HouseholdModel).where(HouseholdModel.id == household_id.value)

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

    async def find_member(
        self, household_id: HouseholdID, user_id: HouseholdUserID
    ) -> Optional[HouseholdMemberDTO]:
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

    async def accept_invite(
        self, household_id: HouseholdID, user_id: HouseholdUserID
    ) -> HouseholdMemberDTO:
        """Accept invite by setting joined_at to current timestamp"""
        # Find the pending invite
        stmt = (
            select(HouseholdMemberModel)
            .where(
                and_(
                    HouseholdMemberModel.household_id == household_id.value,
                    HouseholdMemberModel.user_id == user_id.value,
                    HouseholdMemberModel.joined_at.is_(None),
                    HouseholdMemberModel.left_at.is_(None),
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

    async def revoke_or_remove(
        self, household_id: HouseholdID, user_id: HouseholdUserID
    ) -> None:
        """Revoke invite or remove member by setting left_at to current timestamp"""
        # Find active invite or membership
        stmt = (
            select(HouseholdMemberModel)
            .where(
                and_(
                    HouseholdMemberModel.household_id == household_id.value,
                    HouseholdMemberModel.user_id == user_id.value,
                    HouseholdMemberModel.left_at.is_(None),
                )
            )
            .order_by(HouseholdMemberModel.invited_at.desc())
            .limit(1)
        )

        result = await self._db.execute(stmt)
        member_model = result.scalar_one_or_none()

        if not member_model:
            raise InviteNotFoundError("No active invite or membership found")

        # Set left_at
        member_model.left_at = datetime.now(UTC)

        await self._db.commit()

    async def list_user_households(
        self, user_id: HouseholdUserID
    ) -> List[HouseholdDTO]:
        """List all households user owns or is an active participant in"""
        # Get households where user is owner
        owner_stmt = select(HouseholdModel).where(
            HouseholdModel.owner_user_id == user_id.value
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
                    HouseholdMemberModel.left_at.is_(None),
                )
            )
        )

        # Execute both queries
        owner_result = await self._db.execute(owner_stmt)
        member_result = await self._db.execute(member_stmt)

        owner_households = owner_result.scalars().all()
        member_households = member_result.scalars().all()

        # Combine and dedupe (in case owner is also a member)
        all_households = {h.id: h for h in owner_households}
        all_households.update({h.id: h for h in member_households})

        return [HouseholdMapper.to_dto(h) for h in all_households.values()]

    async def list_user_pending_invites(
        self, user_id: HouseholdUserID
    ) -> List[HouseholdDTO]:
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
                    HouseholdMemberModel.left_at.is_(None),
                )
            )
        )

        result = await self._db.execute(stmt)
        households = result.scalars().all()

        return [HouseholdMapper.to_dto(h) for h in households]

    async def list_household_pending_invites(
        self, household_id: HouseholdID
    ) -> List[HouseholdMemberDTO]:
        """List all pending invites for a household"""
        stmt = select(HouseholdMemberModel).where(
            and_(
                HouseholdMemberModel.household_id == household_id.value,
                HouseholdMemberModel.joined_at.is_(None),
                HouseholdMemberModel.left_at.is_(None),
            )
        )

        result = await self._db.execute(stmt)
        members = result.scalars().all()

        return [HouseholdMemberMapper.to_dto(m) for m in members]

    async def user_has_access(
        self, user_id: HouseholdUserID, household_id: HouseholdID
    ) -> bool:
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
