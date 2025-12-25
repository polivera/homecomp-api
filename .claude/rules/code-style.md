---
paths: app/**/*.py
---

# Python Code Style Guidelines

## General Python Style

- Follow PEP 8 with line length limit of 100 characters
- Use Python 3.13+ features where beneficial
- Prefer `dataclass` over manual `__init__` methods
- Use `frozen=True` for immutable data structures
- Use type hints for ALL function signatures and class attributes

## Type Hints

### Always Annotate

```python
# Good
async def find_user(self, email: Email) -> Optional[UserDTO]:
    pass

# Bad
async def find_user(self, email):
    pass
```

### Use Domain Types

```python
# Good - uses value objects
def create_user(email: Email, password: Password) -> UserID:
    pass

# Bad - uses primitives
def create_user(email: str, password: str) -> int:
    pass
```

### SQLAlchemy Type Annotations

```python
from sqlalchemy.orm import Mapped, mapped_column

class UserModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
```

## Async/Await Conventions

### Always Use Async

All application code should be async:

```python
# Good
async def login(self, email: Email, password: Password) -> LoginResult:
    user = await self._user_repo.find_user(email=email)
    return result

# Bad - blocking in async context
async def login(self, email: Email, password: Password) -> LoginResult:
    user = self._user_repo.find_user_sync(email=email)  # Blocks!
    return result
```

### Await Database Operations

```python
# Good
result = await db.execute(select(UserModel).where(...))

# Bad
result = db.execute(select(UserModel).where(...))  # Missing await!
```

## Dataclasses and Immutability

### Value Objects

Always frozen, with validation in `__post_init__`:

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Email:
    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        # Only validate if not from trusted source
        if not self._validated and not self._is_valid():
            raise ValueError(f"Invalid email: {self.value}")

    @classmethod
    def from_trusted_source(cls, value: str) -> "Email":
        """
        Create Email from trusted source (e.g., database) - skips validation.
        Use this to avoid performance overhead when data is already validated.
        """
        return cls(value, _validated=True)

    def _is_valid(self) -> bool:
        # Validation logic
        return True
```

**Usage:**

```python
# From user input - validates
user_email = Email("user@example.com")  # Runs validation

# From database - skips validation for performance
class UserMapper:
    @staticmethod
    def toDTO(model: UserModel) -> UserDTO:
        return UserDTO(
            user_id=UserID(model.id),
            email=Email.from_trusted_source(model.email),  # No validation overhead
            password=Password.from_hash(model.password)
        )
```

### DTOs

Always frozen, minimal logic:

```python
@dataclass(frozen=True)
class UserDTO:
    user_id: UserID
    email: Email
    password: Password
```

### Pydantic Models

Use for request validation only (interface layer):

```python
class LoginRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    email: EmailStr
    password: str
```

## Error Handling

### Value Objects

Raise `ValueError` for validation failures:

```python
def __post_init__(self):
    if len(self.value) < 8:
        raise ValueError("Password must be at least 8 characters")
```

### Domain Services

Create domain-specific exceptions:

```python
class AuthenticationError(Exception):
    pass

class LoginService:
    async def login(...) -> LoginResult:
        if not user:
            raise AuthenticationError("Invalid credentials")
```

### Controllers

Convert to HTTP exceptions:

```python
from fastapi import HTTPException

@router.post("/login")
async def login(request: LoginRequest):
    try:
        result = await handler.handle(...)
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
```

## Import Organization

Group imports in this order:

1. Standard library
2. Third-party packages (FastAPI, SQLAlchemy, etc.)
3. Local application imports (absolute imports from `app.*`)

```python
# Standard library
from dataclasses import dataclass
from typing import Optional

# Third-party
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Local application
from app.context.auth.domain.contracts.login_service_contract import LoginServiceContract
from app.context.auth.application.commands.login_command import LoginCommand
from app.shared.domain.value_objects.shared_email import Email as SharedEmail
```

## Dependency Injection

### Define Contract-Based Factories

```python
# infrastructure/dependencies.py
def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepositoryContract:
    return UserRepository(db)

def get_login_handler(
    service: LoginServiceContract = Depends(get_login_service),
) -> LoginHandlerContract:
    return LoginHandler(service)
```

### Inject in Controllers

```python
@router.post("/login")
async def login(
    request: LoginRequest,
    handler: LoginHandlerContract = Depends(get_login_handler),
):
    command = LoginCommand(...)
    return await handler.handle(command)
```

## Naming Conventions

### Files

- Contracts: `{name}_contract.py`
- Implementations: `{name}.py`
- DTOs: `{name}_dto.py`
- Commands: `{action}_command.py`
- Queries: `{action}_query.py`
- Handlers: `{action}_handler.py`

### Classes

- Contracts: `{Name}Contract` (e.g., `LoginServiceContract`)
- Implementations: `{Name}` (e.g., `LoginService`)
- DTOs: `{Name}DTO` (e.g., `UserDTO`)
- Value Objects: `{Name}` (e.g., `Email`, `Password`)

### Variables

- Use descriptive names: `user_repository` not `repo`
- Private attributes: `self._db`, `self._user_repo`
- Constants: `MAX_LOGIN_ATTEMPTS = 5`

## Documentation

### Docstrings

Use for public APIs and complex business logic:

```python
async def find_user(self, email: Email) -> Optional[UserDTO]:
    """
    Find a user by email address.

    Args:
        email: The user's email address

    Returns:
        UserDTO if found, None otherwise
    """
    pass
```

### Comments

Only when the "why" isn't obvious from the code:

```python
# Bad - states the obvious
# Increment the counter
counter += 1

# Good - explains the business reason
# Argon2 recommends time_cost=2 for interactive logins
hasher = PasswordHasher(time_cost=2)
```

## Code Organization Within Files

Standard order within a class:

1. Class variables
2. `__init__` or dataclass fields
3. Public methods
4. Private methods
5. Static/class methods

```python
@dataclass(frozen=True)
class Example:
    # Fields
    field: str

    # Public methods
    def public_method(self):
        pass

    # Private methods
    def _private_helper(self):
        pass

    # Static methods
    @staticmethod
    def static_helper():
        pass
```
