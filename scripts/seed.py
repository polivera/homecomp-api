import asyncio
import sys
from pathlib import Path

from app.context.user.domain.value_objects.password import Password
from app.context.user.infrastructure.models import UserModel
from app.shared.infrastructure.database import AsyncSessionLocal

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


async def seed():
    passwd = Password.from_plain_text("testonga")
    async with AsyncSessionLocal() as session:
        # Add your seed data
        print("Seeding users")
        users = [
            UserModel(email="user1@test.com", password=passwd.value),
            UserModel(email="user2@test.com", password=passwd.value),
        ]
        session.add_all(users)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
