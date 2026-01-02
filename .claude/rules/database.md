---
paths: "{app/**/infrastructure/**/*.py,migrations/**/*.py}"
---

# Database and Migration Guidelines

## SQLAlchemy Async Patterns

### Session Management

Always use dependency injection for database sessions:

```python
from app.shared.infrastructure.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

async def my_handler(db: AsyncSession = Depends(get_db)):
    # Session is automatically managed
    result = await db.execute(...)
    await db.commit()  # If needed
```

Never create sessions manually in application code.

### Model Registration

**CRITICAL**: All SQLAlchemy models must be imported to register them with the metadata **before** any database operations occur. This is especially important for models with foreign key relationships.

**Pattern**: Import all models at the **end** of `app/shared/infrastructure/database.py`:

```python
# app/shared/infrastructure/database.py

# ... database setup code ...

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# ──────────────────────────────────────────────────────────────────────────────
# Import all models to register them with SQLAlchemy metadata
# IMPORTANT: Order matters! Parent tables must be imported before child tables
# ──────────────────────────────────────────────────────────────────────────────

from app.context.user.infrastructure.models.user_model import UserModel  # noqa: F401, E402
from app.context.user_account.infrastructure.models.user_account_model import (  # noqa: F401, E402
    UserAccountModel,
)
from app.context.auth.infrastructure.models.session_model import SessionModel  # noqa: F401, E402
from app.context.credit_card.infrastructure.models.credit_card_model import (  # noqa: F401, E402
    CreditCardModel,
)
```

**Why this works**:
1. Models import `BaseDBModel` from `app.shared.infrastructure.models` (just the base class)
2. `database.py` imports model classes directly at the end (after all setup is complete)
3. No circular imports because dependency flows one way
4. Models are automatically registered when `database.py` is imported (which happens via `get_db()`)

**Import Order Rules**:
- Parent tables (referenced by foreign keys) must come **before** child tables
- Example: `users` → `user_accounts` → `credit_cards` (since credit_cards references user_accounts)

**Why NOT in other places**:
- ❌ **NOT in `models/__init__.py`** - causes circular imports (models import BaseDBModel from there)
- ❌ **NOT in `main.py`** - pollutes application entry point, not the right responsibility
- ❌ **NOT in individual model files** - would require every model to know about all other models
- ✅ **YES in `database.py`** - centralized, runs automatically, no circular dependency

**When adding new models**:
1. Add import to `database.py` at the end
2. Place it in correct order based on foreign key dependencies
3. Use `# noqa: F401, E402` to suppress linter warnings (F401=unused import, E402=import not at top)

### Query Execution

Use async patterns with proper await:

```python
# SELECT queries
stmt = select(UserModel).where(UserModel.email == email)
result = await db.execute(stmt)
user = result.scalar_one_or_none()

# INSERT
db.add(user_model)
await db.commit()
await db.refresh(user_model)

# UPDATE
stmt = update(UserModel).where(UserModel.id == user_id).values(email=new_email)
await db.execute(stmt)
await db.commit()

# DELETE
stmt = delete(UserModel).where(UserModel.id == user_id)
await db.execute(stmt)
await db.commit()
```

### Result Handling

```python
# Single result (raises if not found)
user = result.scalar_one()

# Single result (returns None if not found)
user = result.scalar_one_or_none()

# Multiple results
users = result.scalars().all()

# First result
user = result.scalars().first()
```

## Database Models

### Base Model Usage

All models must inherit from `BaseModel`:

```python
from app.shared.infrastructure.models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC

class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
```

### Type Annotations

Use `Mapped[type]` for all columns:

```python
# Basic types
id: Mapped[int]
email: Mapped[str]
is_active: Mapped[bool]

# Optional/nullable
phone: Mapped[Optional[str]] = mapped_column(nullable=True)

# With defaults (see Timezone-Aware Dates section below for datetime)
created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

# Relationships
addresses: Mapped[list["AddressModel"]] = relationship(back_populates="user")
```

### Timezone-Aware Dates

**CRITICAL**: Always use timezone-aware datetime objects in database models to prevent timezone-related bugs.

**Pattern**:

```python
from datetime import datetime, UTC
from sqlalchemy.orm import Mapped, mapped_column

class UserModel(BaseModel):
    __tablename__ = "users"

    # ✅ CORRECT: Timezone-aware with UTC
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False
    )

    # For nullable timestamps
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        default=None,
        nullable=True
    )
```

**Why use `datetime.now(UTC)` wrapped in lambda**:
- `UTC` is a constant from `datetime` module (Python 3.11+)
- Lambda ensures the function is called at insertion time (not model definition time)
- Without lambda, the default would be evaluated once when the class is defined

**Common Mistakes to Avoid**:

```python
# ❌ WRONG: Not timezone-aware
created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

# ❌ WRONG: datetime.utcnow is deprecated and naive
created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.utcnow())

# ❌ WRONG: Missing lambda (evaluates at class definition)
created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

# ✅ CORRECT: Timezone-aware UTC with lambda
created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
```

**Database Column Type**:

PostgreSQL stores timezone-aware timestamps in `TIMESTAMP WITH TIME ZONE`:

```python
# In migrations, Alembic will use TIMESTAMP WITH TIME ZONE automatically
op.add_column('users',
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
)
```

**For Python < 3.11**:

If using Python versions before 3.11, use `timezone.utc`:

```python
from datetime import datetime, timezone

created_at: Mapped[datetime] = mapped_column(
    default=lambda: datetime.now(timezone.utc)
)
```

**Soft Delete Pattern**:

For soft deletes, use nullable `deleted_at`:

```python
class UserModel(BaseModel):
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        default=None,
        nullable=True
    )

    # Query helper properties
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
```

**Benefits of Timezone-Aware Dates**:
- Prevents ambiguity when displaying dates to users in different timezones
- Ensures correct date arithmetic (no DST issues)
- Makes it explicit that all times are stored in UTC
- Required for proper international application support
- Avoids Python warnings about naive datetime comparisons

### Naming Conventions

- Table names: plural snake_case (`users`, `login_attempts`)
- Column names: snake_case (`email`, `created_at`, `is_active`)
- Foreign keys: `{table}_id` (e.g., `user_id`)

## Repository Pattern

### Contract Definition

```python
from abc import ABC, abstractmethod

class UserRepositoryContract(ABC):
    @abstractmethod
    async def find_user(
        self,
        user_id: Optional[UserID] = None,
        email: Optional[Email] = None,
    ) -> Optional[UserDTO]:
        pass

    @abstractmethod
    async def save_user(self, user: UserDTO) -> UserID:
        pass
```

### Implementation

```python
class UserRepository(UserRepositoryContract):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def find_user(
        self,
        user_id: Optional[UserID] = None,
        email: Optional[Email] = None,
    ) -> Optional[UserDTO]:
        stmt = select(UserModel)

        if user_id:
            stmt = stmt.where(UserModel.id == user_id.value)
        if email:
            stmt = stmt.where(UserModel.email == email.value)

        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()

        return UserMapper.toDTO(model) if model else None
```

### Important Rules

- Never return SQLAlchemy models from repositories
- Always use mappers to convert models to DTOs
- Accept domain value objects as parameters (not primitives)
- Return domain DTOs (not database models)
- Keep repositories thin - no business logic

## Mapper Pattern

### Standard Mapper Structure

```python
class UserMapper:
    @staticmethod
    def toDTO(model: UserModel) -> UserDTO:
        """Convert database model to domain DTO"""
        return UserDTO(
            user_id=UserID(model.id),
            email=Email(model.email),
            password=Password.from_hash(model.password),
        )

    @staticmethod
    def toModel(dto: UserDTO) -> UserModel:
        """Convert domain DTO to database model"""
        return UserModel(
            id=dto.user_id.value,
            email=dto.email.value,
            password=dto.password.value,
        )
```

### Mapper Rules

- One mapper per aggregate root
- Static methods only (no state)
- Handle value object conversion
- Place in `infrastructure/mappers/` directory

## Alembic Migrations

### Creating Migrations

Use the Just command:

```bash
# Generate new migration
just migration-generate "add user email verification"

# This runs:
# uv run alembic revision --autogenerate -m "description"
```

### Migration File Structure

```python
"""add user email verification

Revision ID: abc123def456
Revises: previous_revision
Create Date: 2025-12-24 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'abc123def456'
down_revision = 'previous_revision'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('users',
        sa.Column('email_verified', sa.Boolean(), nullable=False, server_default='false')
    )

def downgrade() -> None:
    op.drop_column('users', 'email_verified')
```

### Migration Best Practices

- Always provide both `upgrade()` and `downgrade()`
- Use descriptive migration messages
- Review autogenerated migrations before committing
- Test migrations on a copy of production data
- Keep migrations small and focused
- Add indexes in separate migrations for large tables

### Common Migration Operations

```python
# Add column
op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))

# Drop column
op.drop_column('users', 'phone')

# Create table
op.create_table(
    'login_attempts',
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('email', sa.String(255), nullable=False),
    sa.Column('attempted_at', sa.DateTime(), nullable=False),
)

# Add foreign key
op.create_foreign_key('fk_user_profile', 'profiles', 'users', ['user_id'], ['id'])

# Create index
op.create_index('ix_users_email', 'users', ['email'], unique=True)

# Execute raw SQL (use sparingly)
op.execute("UPDATE users SET is_active = true WHERE created_at > '2025-01-01'")
```

### Running Migrations

```bash
# Apply all pending migrations
just migrate

# This runs:
# uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# See migration history
uv run alembic history

# See current revision
uv run alembic current
```

## Database Connection

### Configuration

Connection details in `.env`:

```
DB_HOST=localhost
DB_PORT=5432
DB_USER=uhomecomp
DB_PASS=homecomppass
DB_NAME=homecomp
```

### Connection Pool Settings

In `app/shared/infrastructure/database.py`:

```python
engine = create_async_engine(
    DATABASE_URL,
    echo=False,              # Set True for SQL logging
    pool_size=5,             # Max persistent connections
    max_overflow=10,         # Max overflow connections
    pool_pre_ping=True,      # Verify connections before use
)
```

## Common Pitfalls

1. **Forgetting await** - All SQLAlchemy async operations need `await`
2. **Returning models from repos** - Always use mappers
3. **N+1 queries** - Use `selectinload()` or `joinedload()` for relationships
4. **Missing transactions** - Use `await db.commit()` for writes
5. **Hardcoded values** - Use value objects, not raw strings/ints
6. **Circular imports** - Forward reference relationships with string `"ModelName"`
7. **Naive datetime objects** - Always use timezone-aware dates with `datetime.now(UTC)`

## Performance Tips

- Use `scalar_one_or_none()` instead of `all()[0]`
- Add indexes on frequently queried columns
- Use `defer()` to skip loading heavy columns
- Use `selectinload()` for one-to-many relationships
- Batch operations when possible
- Consider read replicas for heavy read workloads
