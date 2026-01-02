# Database Seeds

Modular seed data for development and testing.

## Structure

Each table has its own seed file:

- `seed_users.py` - User accounts with hashed passwords
- `seed_households.py` - Household groups
- `seed_household_members.py` - Household memberships (including invitations)
- `seed_user_accounts.py` - Bank accounts in multiple currencies
- `seed_credit_cards.py` - Credit cards with limits and usage

**Note:** Sessions are NOT seeded - they are created dynamically on user login.

## Seed Data

### Users (5 total)
- **john.doe@example.com** (johndoe) - Owner of "Doe Family"
- **jane.smith@example.com** (janesmith) - Owner of "Smith Household"
- **bob.johnson@example.com** (bobjohnson) - Member of "Smith Household"
- **alice.williams@example.com** (alicew) - Owner of "Williams Home"
- **charlie.brown@example.com** (charlieb) - Invited to "Doe Family" (pending)

All users have password: `testonga`

### Households (3 total)
1. **Doe Family** - 3 members (2 active, 1 pending invitation)
2. **Smith Household** - 2 members (both active)
3. **Williams Home** - 1 member (owner only)

### User Accounts (8 total)
- Multi-currency support: USD, EUR, GBP
- Realistic balances ranging from $2,100 to $25,000

### Credit Cards (5 total)
- Various cards with different limits ($3,000 - $15,000)
- Different usage amounts for realistic testing

## Commands

```bash
# Clear all data and reseed
just db-reset

# Clear data only
just db-clear

# Seed data only (will fail if data exists)
just seed
```

## Dependency Order

Seeds are executed in this order to respect foreign key constraints:

1. Users (no dependencies)
2. Households (→ users)
3. User Accounts (→ users)
4. Household Members (→ households, users)
5. Credit Cards (→ users, user_accounts)

**Note:** Sessions are created on login and are not seeded.

## Adding New Seeds

1. Create a new file: `scripts/seeds/seed_<table_name>.py`
2. Define an async function: `async def seed_<table_name>(session, ...dependencies)`
3. Add import to `scripts/seeds/__init__.py`
4. Call the function in `scripts/seed.py` in the correct dependency order
5. Add the table to `scripts/db_clear.py` truncate list (reverse dependency order)

### Template

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.context.<context>.infrastructure.models import <Model>


async def seed_<table_name>(
    session: AsyncSession,
    # Add dependencies as needed (e.g., users: dict[str, UserModel])
) -> dict[str, <Model>]:
    """Seed <table_name> table with test data"""
    print(f"  → Seeding <table_name>...")

    data = [
        # Your seed data here
    ]

    records = [<Model>(**item) for item in data]
    session.add_all(records)
    await session.flush()

    # Return mapping for other seeds to reference
    records_map = {record.key_field: record for record in records}

    print(f"    ✓ Created {len(records)} <table_name>")
    return records_map
```
