from sqlalchemy.ext.asyncio import AsyncSession

from app.context.household.infrastructure.models import HouseholdModel
from app.context.user.infrastructure.models import UserModel


async def seed_households(
    session: AsyncSession, users: dict[str, UserModel]
) -> dict[str, HouseholdModel]:
    """Seed households table with test data"""
    print("  → Seeding households...")

    households_data = [
        {
            "owner_user_id": users["john.doe@example.com"].id,
            "name": "Doe Family",
        },
        {
            "owner_user_id": users["jane.smith@example.com"].id,
            "name": "Smith Household",
        },
        {
            "owner_user_id": users["alice.williams@example.com"].id,
            "name": "Williams Home",
        },
    ]

    households = [HouseholdModel(**data) for data in households_data]
    session.add_all(households)
    await session.flush()

    # Return households as dict for easy reference
    households_map = {household.name: household for household in households}

    print(f"    ✓ Created {len(households)} households")
    return households_map
