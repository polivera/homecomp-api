from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.household.domain.contracts import HouseholdRepositoryContract
from app.context.household.domain.dto import HouseholdDTO
from app.context.household.domain.exceptions import HouseholdNameAlreadyExistError
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdName,
    HouseholdUserID,
)
from app.context.household.infrastructure.mappers import HouseholdMapper
from app.context.household.infrastructure.models import (
    HouseholdModel,
)


class HouseholdRepository(HouseholdRepositoryContract):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create_household(
        self, household_dto: HouseholdDTO, creator_user_id: HouseholdUserID
    ) -> HouseholdDTO:
        """Create a new household with the owner stored in the household table"""

        # Convert DTO to model
        household_model = HouseholdMapper.to_model(household_dto)

        # Add household to database
        self._db.add(household_model)

        try:
            # Commit transaction - will raise IntegrityError if duplicate (owner_user_id, name)
            await self._db.commit()
            await self._db.refresh(household_model)
        except IntegrityError as e:
            await self._db.rollback()
            # Check if it's the unique constraint violation
            if "uq_households_owner_name" in str(e.orig):
                raise HouseholdNameAlreadyExistError(
                    f"Household with name '{household_dto.name.value}' already exists for this user"
                )
            raise Exception(e)

        # Convert back to DTO
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

        return HouseholdMapper.to_dto(model)

    async def find_household_by_id(
        self, household_id: HouseholdID
    ) -> Optional[HouseholdDTO]:
        """Find a household by ID"""

        stmt = select(HouseholdModel).where(HouseholdModel.id == household_id.value)

        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()

        return HouseholdMapper.to_dto(model)
