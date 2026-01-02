from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user.infrastructure.models import UserModel
from app.context.user_account.infrastructure.models import UserAccountModel


async def seed_user_accounts(session: AsyncSession, users: dict[str, UserModel]) -> dict[str, UserAccountModel]:
    """Seed user_accounts table with test data"""
    print("  → Seeding user accounts...")

    accounts_data = [
        # John's accounts
        {
            "user_id": users["john.doe@example.com"].id,
            "name": "Checking Account",
            "currency": "USD",
            "balance": Decimal("5000.00"),
        },
        {
            "user_id": users["john.doe@example.com"].id,
            "name": "Savings Account",
            "currency": "USD",
            "balance": Decimal("15000.50"),
        },
        # Jane's accounts
        {
            "user_id": users["jane.smith@example.com"].id,
            "name": "Main Account",
            "currency": "EUR",
            "balance": Decimal("8500.75"),
        },
        {
            "user_id": users["jane.smith@example.com"].id,
            "name": "Investment Account",
            "currency": "EUR",
            "balance": Decimal("25000.00"),
        },
        # Bob's account
        {
            "user_id": users["bob.johnson@example.com"].id,
            "name": "Personal Account",
            "currency": "GBP",
            "balance": Decimal("3200.25"),
        },
        # Alice's accounts
        {
            "user_id": users["alice.williams@example.com"].id,
            "name": "Checking",
            "currency": "USD",
            "balance": Decimal("7500.00"),
        },
        {
            "user_id": users["alice.williams@example.com"].id,
            "name": "Emergency Fund",
            "currency": "USD",
            "balance": Decimal("10000.00"),
        },
        # Charlie's account
        {
            "user_id": users["charlie.brown@example.com"].id,
            "name": "Main Account",
            "currency": "USD",
            "balance": Decimal("2100.50"),
        },
    ]

    accounts = [UserAccountModel(**data) for data in accounts_data]
    session.add_all(accounts)
    await session.flush()

    # Return accounts as dict for easy reference (key: user_email + account_name)
    accounts_map = {}
    for account in accounts:
        # Find user email by user_id
        user_email = next(email for email, user in users.items() if user.id == account.user_id)
        key = f"{user_email}:{account.name}"
        accounts_map[key] = account

    print(f"    ✓ Created {len(accounts)} user accounts")
    return accounts_map
