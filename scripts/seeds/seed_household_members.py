from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.context.household.infrastructure.models import (
    HouseholdMemberModel,
    HouseholdModel,
)
from app.context.user.infrastructure.models import UserModel


async def seed_household_members(
    session: AsyncSession,
    users: dict[str, UserModel],
    households: dict[str, HouseholdModel],
) -> None:
    """Seed household_members table with test data"""
    print("  → Seeding household members...")

    now = datetime.now(UTC)

    members_data = [
        # Doe Family members
        {
            "household_id": households["Doe Family"].id,
            "user_id": users["john.doe@example.com"].id,
            "role": "owner",
            "joined_at": now,
            "invited_by_user_id": None,  # Owner joined automatically
            "invited_at": None,
        },
        {
            "household_id": households["Doe Family"].id,
            "user_id": users["jane.smith@example.com"].id,
            "role": "participant",
            "joined_at": now,
            "invited_by_user_id": users["john.doe@example.com"].id,
            "invited_at": now,
        },
        {
            "household_id": households["Doe Family"].id,
            "user_id": users["charlie.brown@example.com"].id,
            "role": "participant",
            "joined_at": None,  # Invited but not joined yet
            "invited_by_user_id": users["john.doe@example.com"].id,
            "invited_at": now,
        },
        # Smith Household members
        {
            "household_id": households["Smith Household"].id,
            "user_id": users["jane.smith@example.com"].id,
            "role": "owner",
            "joined_at": now,
            "invited_by_user_id": None,
            "invited_at": None,
        },
        {
            "household_id": households["Smith Household"].id,
            "user_id": users["bob.johnson@example.com"].id,
            "role": "participant",
            "joined_at": now,
            "invited_by_user_id": users["jane.smith@example.com"].id,
            "invited_at": now,
        },
        # Williams Home members
        {
            "household_id": households["Williams Home"].id,
            "user_id": users["alice.williams@example.com"].id,
            "role": "owner",
            "joined_at": now,
            "invited_by_user_id": None,
            "invited_at": None,
        },
    ]

    members = [HouseholdMemberModel(**data) for data in members_data]
    session.add_all(members)
    await session.flush()

    print(f"    ✓ Created {len(members)} household members")
