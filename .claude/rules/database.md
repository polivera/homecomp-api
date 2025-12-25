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

class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
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

# With defaults
created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

# Relationships
addresses: Mapped[list["AddressModel"]] = relationship(back_populates="user")
```

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

## Performance Tips

- Use `scalar_one_or_none()` instead of `all()[0]`
- Add indexes on frequently queried columns
- Use `defer()` to skip loading heavy columns
- Use `selectinload()` for one-to-many relationships
- Batch operations when possible
- Consider read replicas for heavy read workloads
