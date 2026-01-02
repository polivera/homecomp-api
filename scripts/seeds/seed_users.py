from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user.domain.value_objects import UserPassword
from app.context.user.infrastructure.models import UserModel


async def seed_users(session: AsyncSession) -> dict[str, UserModel]:
    """Seed users table with test data"""
    print("  → Seeding users...")

    # Create password once for all test users
    password = UserPassword.from_plain_text("testonga")

    users_data = [
        {
            "email": "john.doe@example.com",
            "username": "johndoe",
            "password": password.value,
        },
        {
            "email": "jane.smith@example.com",
            "username": "janesmith",
            "password": password.value,
        },
        {
            "email": "bob.johnson@example.com",
            "username": "bobjohnson",
            "password": password.value,
        },
        {
            "email": "alice.williams@example.com",
            "username": "alicew",
            "password": password.value,
        },
        {
            "email": "charlie.brown@example.com",
            "username": "charlieb",
            "password": password.value,
        },
    ]

    users = [UserModel(**data) for data in users_data]
    session.add_all(users)
    await session.flush()  # Flush to get IDs without committing

    # Return users as dict for easy reference by other seeders
    users_map = {user.email: user for user in users}

    print(f"    ✓ Created {len(users)} users")
    return users_map
