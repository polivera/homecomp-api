import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text

from app.shared.infrastructure.database import AsyncSessionLocal


async def clear_database():
    """
    Clear all data from the database tables in reverse dependency order.
    This allows re-seeding without dropping and recreating the database.
    """
    async with AsyncSessionLocal() as session:
        print("\n🗑️  Clearing database...\n")

        try:
            # Truncate in reverse dependency order (children before parents)
            tables = [
                "credit_cards",
                "household_members",
                "user_accounts",
                "households",
                "sessions",
                "users",
            ]

            for table in tables:
                await session.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
                print(f"  ✓ Cleared {table}")

            await session.commit()
            print("\n✅ Database cleared successfully!\n")

        except Exception as e:
            await session.rollback()
            print(f"\n❌ Clear failed: {e}\n")
            raise


if __name__ == "__main__":
    asyncio.run(clear_database())
