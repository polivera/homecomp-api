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
│   └── dependencies.py # Dependency injection setup
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

### 1. Dependency Injection via FastAPI

Dependencies are defined as factory functions in `infrastructure/dependencies.py`:

```python
# Pattern: Contract-based injection
def get_service() -> ServiceContract:
    return ConcreteService()

def get_handler(
    service: ServiceContract = Depends(get_service),
) -> HandlerContract:
    return ConcreteHandler(service)
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
   - Dependencies
5. **Add interface layer**:
   - Pydantic schemas
   - Controllers
   - Route registration in `app/main.py`
6. **Create database migration**:
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
