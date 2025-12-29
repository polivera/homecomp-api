from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.context.credit_card.infrastructure.models import CreditCardModel
from app.context.user.infrastructure.models import UserModel
from app.context.user_account.infrastructure.models import UserAccountModel


async def seed_credit_cards(
    session: AsyncSession,
    users: dict[str, UserModel],
    accounts: dict[str, UserAccountModel],
) -> None:
    """Seed credit_cards table with test data"""
    print("  → Seeding credit cards...")

    cards_data = [
        # John's credit cards
        {
            "user_id": users["john.doe@example.com"].id,
            "account_id": accounts["john.doe@example.com:Checking Account"].id,
            "name": "Visa Platinum",
            "currency": "USD",
            "limit": Decimal("10000.00"),
            "used": Decimal("2500.50"),
        },
        {
            "user_id": users["john.doe@example.com"].id,
            "account_id": accounts["john.doe@example.com:Checking Account"].id,
            "name": "Mastercard Gold",
            "currency": "USD",
            "limit": Decimal("5000.00"),
            "used": Decimal("1200.00"),
        },
        # Jane's credit card
        {
            "user_id": users["jane.smith@example.com"].id,
            "account_id": accounts["jane.smith@example.com:Main Account"].id,
            "name": "Amex Blue",
            "currency": "EUR",
            "limit": Decimal("8000.00"),
            "used": Decimal("3500.75"),
        },
        # Alice's credit card
        {
            "user_id": users["alice.williams@example.com"].id,
            "account_id": accounts["alice.williams@example.com:Checking"].id,
            "name": "Chase Sapphire",
            "currency": "USD",
            "limit": Decimal("15000.00"),
            "used": Decimal("4200.00"),
        },
        # Bob's credit card
        {
            "user_id": users["bob.johnson@example.com"].id,
            "account_id": accounts["bob.johnson@example.com:Personal Account"].id,
            "name": "Discover Card",
            "currency": "GBP",
            "limit": Decimal("3000.00"),
            "used": Decimal("800.25"),
        },
    ]

    cards = [CreditCardModel(**data) for data in cards_data]
    session.add_all(cards)
    await session.flush()

    print(f"    ✓ Created {len(cards)} credit cards")
