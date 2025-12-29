import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import all seed functions
from seeds import (
    seed_credit_cards,
    seed_household_members,
    seed_households,
    seed_user_accounts,
    seed_users,
)

from app.shared.infrastructure.database import AsyncSessionLocal


async def seed():
    async with AsyncSessionLocal() as session:
        print("\n🌱 Starting database seeding...\n")

        try:
            # Seed in dependency order
            users = await seed_users(session)
            households = await seed_households(session, users)
            accounts = await seed_user_accounts(session, users)
            await seed_household_members(session, users, households)
            await seed_credit_cards(session, users, accounts)

            # Commit all changes
            await session.commit()

            print("\n✅ Database seeding completed successfully!\n")

        except Exception as e:
            await session.rollback()
            print(f"\n❌ Seeding failed: {e}\n")
            raise


if __name__ == "__main__":
    asyncio.run(seed())
