# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**HomeComp API** is a FastAPI-based REST API following **Domain-Driven Design (DDD)** principles. The application is structured around bounded contexts with clear separation between domain logic, application orchestration, infrastructure, and interface layers.

## Technology Stack

- **Python 3.13+** (required)
- **FastAPI 0.125.0** - Async web framework
- **SQLAlchemy 2.0.45** - Async ORM
- **PostgreSQL 16** - Database
- **Alembic 1.17.2** - Database migrations
- **Argon2** - Password hashing
- **UV** - Python package manager
- **Just** - Command runner

## Development Commands

### Running the Application

```bash
# Start development server (with auto-reload)
just run
# Runs: uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

The API will be available at:
- **API**: http://localhost:8080
- **Docs**: http://localhost:8080/docs (Swagger UI)
- **Redoc**: http://localhost:8080/redoc

### Database Operations

```bash
# Generate a new migration
just migration-generate "description of changes"

# Run pending migrations
just migrate

# Connect to PostgreSQL CLI
just pgcli
```

### Docker Services

```bash
# Start PostgreSQL container
docker-compose up -d

# Stop all services
docker-compose down
```

## Architecture

### DDD Layered Structure

The codebase follows a strict 4-layer DDD architecture within each bounded context:

```
app/context/{context_name}/
├── domain/              # Core business logic (framework-agnostic)
│   ├── contracts/       # Service interfaces (dependency inversion)
│   ├── services/        # Domain services (business rules)
│   ├── value_objects/   # Immutable validated objects
│   └── dto/            # Domain data transfer objects
│
├── application/        # Use cases and orchestration
│   ├── commands/       # Write operations (CQRS)
│   ├── queries/        # Read operations (CQRS)
│   ├── handlers/       # Command/query handler implementations
│   ├── contracts/      # Handler interfaces
│   └── dto/           # Application DTOs
│
├── infrastructure/     # External concerns and implementations
│   ├── repositories/   # Data access implementations
│   ├── models/        # SQLAlchemy ORM models
│   ├── mappers/       # Domain DTO ↔ Database model mappers
│   └── dependencies/  # Dependency injection factory functions
│       ├── dependencies.py
│       └── __init__.py
│
└── interface/         # External interfaces
    └── rest/          # REST API layer
        ├── controllers/  # FastAPI route handlers
        ├── schemas/     # Pydantic request/response models
        └── routes.py    # Router registration
```

### Current Bounded Contexts

1. **Auth Context** (`app/context/auth/`) - Authentication and authorization
2. **User Context** (`app/context/user/`) - User management
3. **Category Context** (`app/context/category/`) - Global category management

### Domain Design Rules

**CRITICAL**: These rules must be followed to maintain proper domain separation:

1. **Categories are Global and Independent**
   - Categories belong to users but are **NOT** tied to households
   - A category can be used across multiple households
   - **Never** add a `household_id` foreign key to the categories table
   - Categories are user-scoped, not household-scoped
   - This ensures flexibility: users can reuse categories across different households

### Shared Kernel

Located at `app/shared/`, contains cross-cutting concerns:

- **Infrastructure**:
  - `database.py` - Async SQLAlchemy engine and session factory
  - `models/base_model.py` - Base database model

- **Domain**:
  - `value_objects/shared_email.py` - Email validation
  - `value_objects/shared_password.py` - Argon2 password hashing

## Key Architectural Patterns

**IMPORTANT**: For comprehensive details on implementing DDD and CQRS patterns, see `/docs/ddd-patterns.md`. This includes:
- When to use Commands vs Queries
- Complete data flow diagrams for both
- Interface (contract) definitions and placement
- Dependency injection setup and rules
- Cross-context communication patterns
- Common anti-patterns to avoid

### 1. Dependency Injection via ApplicationContainer

Dependencies are managed through a centralized **ApplicationContainer** (`app/shared/infrastructure/container/app_container.py`) that provides all handlers with their dependencies already wired.

**Infrastructure Layer** - Define factory functions in `infrastructure/dependencies/dependencies.py`:

```python
# Factory pattern: Takes db and logger, returns fully configured handler
def login_handler_factory(db: AsyncSession, logger: LoggerContract) -> LoginHandlerContract:
    """Factory for LoginHandler with all dependencies"""
    from app.context.auth.infrastructure.repositories import SessionRepository
    from app.context.auth.domain.services import LoginService
    from app.context.auth.application.handlers import LoginHandler
    from app.context.user.infrastructure.dependencies import find_user_handler_factory

    # Wire up dependencies
    session_repo = SessionRepository(db)
    login_service = LoginService(session_repo, logger)
    user_handler = find_user_handler_factory(db, logger)

    return LoginHandler(user_handler, login_service, logger)
```

**ApplicationContainer** - Centralizes dependency management:

```python
# app/shared/infrastructure/container/app_container.py
class ApplicationContainer:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._logger = get_logger()

    @property
    def logger(self) -> LoggerContract:
        return self._logger

    def get_login_handler(self):
        """Get login handler with all dependencies"""
        from app.context.auth.infrastructure.dependencies import login_handler_factory
        return login_handler_factory(self._db, self._logger)
```

**Controllers** - Inject ApplicationContainer via FastAPI:

```python
from typing import Annotated
from fastapi import APIRouter, Depends
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container

@router.post("/login")
async def login(
    request: LoginRequest,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
):
    logger = app_container.logger
    handler = app_container.get_login_handler()

    command = LoginCommand(...)
    return await handler.handle(command)
```

**Important**: Always program to contracts (interfaces), not implementations.

### 2. CQRS (Command Query Responsibility Segregation)

- **Commands** - Represent write operations (e.g., `LoginCommand`)
- **Queries** - Represent read operations (e.g., `FindUserQuery`)
- **Handlers** - Process commands/queries and coordinate domain services

### 3. Repository Pattern

All data access goes through repository contracts:

```python
# Contract defines interface
class UserRepositoryContract(ABC):
    async def find_user(self, user_id: Optional[UserID] = None) -> Optional[UserDTO]:
        pass

# Implementation uses SQLAlchemy
class UserRepository(UserRepositoryContract):
    def __init__(self, db: AsyncSession):
        self._db = db
```

### 4. Mapper Pattern

Separate database models from domain DTOs using mappers:

```python
class UserMapper:
    @staticmethod
    def toDTO(model: UserModel) -> UserDTO:
        return UserDTO(
            user_id=UserID(model.id),
            email=Email(model.email),
            password=Password.from_hash(model.password)
        )
```

**Rule**: Never pass SQLAlchemy models outside the infrastructure layer.

### 5. Value Objects

Use immutable, validated value objects for domain concepts:

```python
@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        # Validation logic here
        if not self._is_valid():
            raise ValueError(f"Invalid email: {self.value}")
```

#### Context-Specific Value Objects

**Rule**: To maintain bounded context isolation, **always create context-specific value objects** even when they share identical validation logic.

**Pattern**:
1. Define validation logic once in the **Shared Kernel** (`app/shared/domain/value_objects/`)
2. Create **context-specific wrappers** that extend the shared value object
3. Each context uses **only its own value object types**, never shared or cross-context types

**Example**:

```python
# Shared Kernel - contains validation logic
# app/shared/domain/value_objects/shared_currency.py
@dataclass(frozen=True)
class SharedCurrency:
    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if len(self.value) != 3:
                raise ValueError("Currency code must be 3 characters")
            if not self.value.isupper():
                raise ValueError("Currency code must be uppercase")

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        return cls(value, _validated=True)

# User Account Context - extends shared validation
# app/context/user_account/domain/value_objects/account_currency.py
@dataclass(frozen=True)
class UserAccountCurrency(SharedCurrency):
    pass

# Credit Card Context - extends shared validation
# app/context/credit_card/domain/value_objects/credit_card_currency.py
@dataclass(frozen=True)
class CreditCardCurrency(SharedCurrency):
    pass
```

**Usage**:

```python
# Good - each context uses its own type
class UserAccountDTO:
    currency: UserAccountCurrency  # ✅ Context-specific type

class CreditCardDTO:
    currency: CreditCardCurrency   # ✅ Context-specific type

# Bad - using shared type directly
class UserAccountDTO:
    currency: SharedCurrency       # ❌ Breaks context isolation

# Bad - cross-context usage
class UserAccountDTO:
    currency: CreditCardCurrency   # ❌ Wrong context!
```

**Benefits**:
- **Context Isolation**: Maintains clear bounded context boundaries
- **No Code Duplication**: Validation logic lives in one place (shared kernel)
- **Type Safety**: Prevents accidental mixing of types from different contexts
- **Future Flexibility**: Contexts can add specific behavior later without affecting others
- **Explicit Domain Modeling**: Code clearly shows which context a value belongs to

**When to Use**:
- Apply this pattern to **all value objects that appear in multiple contexts**
- Common examples: Currency, Money, Quantity, Percentage, Date/Time ranges
- Even if contexts share identical validation today, use context-specific types for future flexibility

### 6. Authentication in Controllers

**Rule**: Controllers obtain the authenticated user ID via dependency injection from shared middleware. The user ID is passed as a **primitive** (int) to commands/queries, following CQRS principles.

**Pattern**:

```python
# Controller - app/context/user_account/interface/rest/controllers/create_account_controller.py
from typing import Annotated
from fastapi import APIRouter, Depends
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

@router.post("/accounts", status_code=201)
async def create_account(
    request: CreateAccountRequest,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],  # ✅ Inject authenticated user ID
):
    # Get dependencies from container
    logger = app_container.logger
    handler = app_container.get_create_account_handler()

    # Pass primitive user_id to command
    command = CreateAccountCommand(
        user_id=user_id,        # ✅ Primitive in command
        name=request.name,
        currency=request.currency,
        balance=request.balance,
    )
    result = await handler.handle(command)
    return result
```

**Middleware Implementation**:

The shared middleware (`app/shared/infrastructure/middleware/session_auth_dependency.py`) provides two authentication dependencies:

```python
async def get_current_user_id(
    access_token: Optional[str] = Cookie(default=None),
    session_repo: SessionRepositoryContract = Depends(get_session_repository_for_auth),
) -> int:
    """
    Required authentication - raises 401 if not authenticated.
    Returns: user_id as int
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = SessionToken(access_token)
    session = await session_repo.getSession(token=token)

    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    return session.user_id.value  # Extract primitive from value object


async def get_current_user_id_optional(
    access_token: Optional[str] = Cookie(default=None),
    session_repo: SessionRepositoryContract = Depends(get_session_repository_for_auth),
) -> Optional[int]:
    """
    Optional authentication - returns None if not authenticated.
    Returns: Optional[int]
    """
    if not access_token:
        return None

    # ... validation logic ...
    return session.user_id.value if session else None
```

**Command Structure**:

Commands receive user_id as a primitive:

```python
# app/context/user_account/application/commands/create_account_command.py
@dataclass(frozen=True)
class CreateAccountCommand:
    user_id: int      # ✅ Primitive type (not UserID value object)
    name: str
    currency: str
    balance: float
```

**Handler Converts to Value Objects**:

```python
# app/context/user_account/application/handlers/create_account_handler.py
class CreateAccountHandler:
    async def handle(self, command: CreateAccountCommand) -> CreateAccountResult:
        # Convert primitives to value objects
        user_id = UserID(command.user_id)  # ✅ Handler creates value objects
        name = AccountName(command.name)
        currency = UserAccountCurrency(command.currency)

        # Use value objects in domain service
        account_dto = await self._service.create_account(
            user_id=user_id,
            name=name,
            currency=currency,
        )
        return result
```

**Authentication Flow**:

```
1. HTTP Request with Cookie
   ↓
2. get_current_user_id dependency
   → Extracts access_token from cookie
   → Validates SessionToken value object
   → Queries SessionRepository
   → Returns int (user_id.value)
   ↓
3. Controller receives user_id: int
   → Creates Command with primitive user_id
   ↓
4. Handler receives Command
   → Converts user_id to UserID value object
   → Passes to domain service
```

**When to Use**:

- **Required Authentication**: Use `get_current_user_id` - raises 401 if not authenticated
- **Optional Authentication**: Use `get_current_user_id_optional` - returns None if not authenticated (e.g., personalized public content)

**Benefits**:

- **Centralized Authentication**: All auth logic in one place (middleware)
- **Separation of Concerns**: Controllers don't handle token validation
- **CQRS Compliance**: Commands use primitives, handlers use value objects
- **Type Safety**: FastAPI validates dependency types automatically
- **Testability**: Easy to mock user_id in tests

## Database Configuration

### Connection Details

Configuration in `.env`:
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=uhomecomp
DB_PASS=homecomppass
DB_NAME=homecomp
```

### Session Management

Get async database sessions via dependency injection:

```python
from app.shared.infrastructure.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

async def my_handler(db: AsyncSession = Depends(get_db)):
    # Use db session here
```

### Migrations

- All migrations live in `/migrations/`
- Use Alembic for schema changes
- Migration environment imports from `app.shared.infrastructure.models.base_model`

## Security Considerations

### Password Hashing

Always use `SharedPassword` value object for password operations:

```python
# Hashing
hashed = SharedPassword.from_plain_text("user_password")

# Verification
is_valid = hashed_password.verify("input_password")
```

Uses **Argon2** algorithm (modern, secure).

### Login Throttling

Comprehensive implementation guide available at `/docs/login-throttle-implementation.md`.

**Recommended approach**:
- **Development**: In-memory throttle service
- **Production**: Redis-based throttle service (distributed, persistent)

Throttle by **email** (not just IP) to prevent account-specific brute-force attacks.

## Code Organization Rules

### Layer Dependencies

Dependencies flow in ONE direction only:

```
Interface → Application → Domain
   ↓            ↓
Infrastructure ←┘
```

**Rules**:
- Domain layer has NO dependencies on other layers
- Application layer depends ONLY on domain
- Infrastructure implements domain contracts
- Interface layer orchestrates via application handlers

### Cross-Context Communication

When one context needs data from another:

1. Import the **query handler contract** from the other context's application layer
2. Inject via dependency injection
3. Never access repositories directly across contexts

**Example**: Auth context uses `FindUserHandlerContract` from User context.

### File Naming Conventions

- **Contracts/Interfaces**: `{name}_contract.py`
- **Implementations**: `{name}.py`
- **DTOs**: `{name}_dto.py`
- **Value Objects**: `{name}.py` (e.g., `email.py`, `password.py`)
- **Commands**: `{action}_command.py`
- **Queries**: `{action}_query.py`
- **Handlers**: `{action}_handler.py`

## Data Flow Example

Typical request flow through the system:

```
1. HTTP Request
   ↓
2. Pydantic Schema (interface/rest/schemas)
   ↓
3. Controller (interface/rest/controllers)
   ↓
4. Handler (application/handlers)
   → Converts to Command/Query
   ↓
5. Domain Service (domain/services)
   → Contains business logic
   ↓
6. Repository (infrastructure/repositories)
   → Data access via SQLAlchemy
   → Returns Domain DTO (via Mapper)
   ↓
7. Handler returns Application DTO
   ↓
8. Controller returns Pydantic response
```

## Important Implementation Notes

### Async/Await

This is an **async-first** codebase:
- All route handlers are `async def`
- All repository methods are `async`
- Use `await` for database operations
- Database sessions are async (`AsyncSession`)

### Type Hints

Extensive type hints are used throughout:
- All function parameters and return types should be annotated
- Use domain types (Value Objects, DTOs) instead of primitives
- SQLAlchemy uses `Mapped[]` type annotations

### REST Schemas

When creating schemas for the REST interface layer:

**Request Schemas** (incoming data):
- Use **Pydantic `BaseModel`** for validation
- Set `model_config = ConfigDict(frozen=True)` for immutability
- Leverage Pydantic validators (`EmailStr`, custom validators, etc.)

**Response Schemas** (outgoing data):
- Use **Python `@dataclass(frozen=True)`** for simplicity
- No validation needed (we control the data)
- Avoids unnecessary Pydantic overhead
- FastAPI can serialize dataclasses automatically

```python
# Request schema - use Pydantic for validation
class LoginRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    email: EmailStr
    password: str

# Response schema - use dataclass for performance
@dataclass(frozen=True)
class LoginResponse:
    message: str
```

### Error Handling

When implementing new features:
- Raise `ValueError` in value objects for validation failures
- Raise `HTTPException` in controllers for HTTP errors
- Domain services should raise domain-specific exceptions
- Let FastAPI handle exception-to-HTTP conversion

## Current Implementation Status

### Completed
- User context with repository and query handler
- Auth context scaffolding
- Database models and migrations for users
- Dependency injection setup
- Password hashing with Argon2
- Value objects for Email, Password, UserID

### In Progress
- Login service implementation (see `app/context/auth/domain/services/login_service.py:10-15`)
- Login throttling (see `/docs/login-throttle-implementation.md`)
- Token generation for authentication

## Testing Guidelines

No test suite currently exists. When implementing tests:

### Structure
```
tests/
├── unit/
│   ├── context/
│   │   ├── auth/
│   │   │   ├── domain/      # Test domain services, value objects
│   │   │   ├── application/ # Test handlers
│   │   │   └── infrastructure/ # Test repositories (with test DB)
│   │   └── user/
│   └── shared/
└── integration/
    └── test_api_endpoints.py
```

### Recommendations
- Use `pytest` with `pytest-asyncio`
- Mock repository contracts for unit tests
- Use test database for integration tests
- Test value object validation extensively
- Test CQRS handlers with mocked dependencies

## Common Pitfalls to Avoid

1. **Don't bypass value objects** - Always use `Email`, `Password`, etc., never raw strings
2. **Don't skip the mapper layer** - Never return SQLAlchemy models from repositories
3. **Don't mix contexts directly** - Use query handlers for cross-context communication
4. **Don't put business logic in controllers** - Keep it in domain services
5. **Don't forget dependency injection** - Use `Depends()` for all dependencies
6. **Don't use sync database operations** - Everything must be async
7. **Don't violate layer dependencies** - Domain should never import from infrastructure

## Adding New Features

When implementing a new feature:

1. **Identify the bounded context** - Does it fit in Auth, User, or need a new context?
2. **Design domain layer first**:
   - Value objects
   - Domain DTOs
   - Service contracts
   - Domain services
3. **Create application layer**:
   - Commands/Queries
   - Handler contracts
   - Handler implementations
4. **Implement infrastructure**:
   - Database models (if needed)
   - Repositories
   - Mappers
   - Factory functions in `dependencies/dependencies.py`
   - Export factories in `dependencies/__init__.py`
5. **Register in ApplicationContainer**:
   - Add handler getter method(s) to `app/shared/infrastructure/container/app_container.py`
   - Method should call the factory function with `self._db` and `self._logger`
6. **Add interface layer**:
   - Pydantic schemas
   - Controllers (using `ApplicationContainer` pattern)
   - Route registration in `app/main.py`
7. **Create database migration**:
   - `just migration-generate "description"`
   - `just migrate`

## Package Management

This project uses **UV** (not pip):

```bash
# Install dependencies
uv sync

# Add new dependency
uv add package-name

# Add dev dependency
uv add --dev package-name
```

Dependencies are locked in `uv.lock` and declared in `pyproject.toml`.
