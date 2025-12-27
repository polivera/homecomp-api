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

### Custom Exceptions for Each Case

**ALWAYS create specific custom exceptions** instead of raising standard exceptions (ValueError, RuntimeError, etc.). Each exceptional case should have its own exception class.

**Rationale:**
- Makes error handling more explicit and type-safe
- Allows different handling for different error cases
- Self-documenting code (exception name describes what went wrong)
- Easier to catch and handle specific errors in controllers

### Exception Organization

Create exceptions in `domain/exceptions/`:

```python
# app/context/user_account/domain/exceptions/exceptions.py
class UserAccountMapperError(Exception):
    pass

class UserAccountNameAlreadyExistError(Exception):
    pass

class UserAccountNotFoundError(Exception):
    pass
```

```python
# app/context/user_account/domain/exceptions/__init__.py
from .exceptions import (
    UserAccountMapperError,
    UserAccountNameAlreadyExistError,
    UserAccountNotFoundError,
)

__all__ = [
    "UserAccountMapperError",
    "UserAccountNameAlreadyExistError",
    "UserAccountNotFoundError",
]
```

### Naming Convention

Exception names should clearly describe the error condition:

- `{Entity}NotFoundError` - Entity doesn't exist
- `{Entity}{Field}AlreadyExistError` - Duplicate/unique constraint violation
- `{Entity}{Operation}Error` - Operation-specific failures
- `Invalid{Entity}{Field}Error` - Validation failures for specific fields

```python
# Good - specific exceptions
class UserNotFoundError(Exception):
    pass

class UserEmailAlreadyExistError(Exception):
    pass

class InvalidUserPasswordError(Exception):
    pass

# Bad - generic exceptions
raise ValueError("User not found")  # Don't do this!
raise RuntimeError("Email already exists")  # Don't do this!
```

### Value Objects

Create specific validation exceptions:

```python
# app/context/user/domain/exceptions/exceptions.py
class InvalidEmailFormatError(Exception):
    pass

class InvalidPasswordLengthError(Exception):
    pass

# app/context/user/domain/value_objects/email.py
@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self._is_valid():
            raise InvalidEmailFormatError(
                f"Invalid email format: '{self.value}'. "
                f"Expected format: user@domain.com"
            )
```

### Domain Services

Raise specific domain exceptions:

```python
# app/context/auth/domain/exceptions/exceptions.py
class InvalidCredentialsError(Exception):
    pass

class AccountLockedError(Exception):
    pass

# app/context/auth/domain/services/login_service.py
class LoginService:
    async def login(...) -> LoginResult:
        user = await self._user_repo.find_user(email=email)
        if not user:
            raise InvalidCredentialsError("Invalid email or password")

        if user.is_locked:
            raise AccountLockedError(f"Account locked until {user.locked_until}")
```

### Controllers

Map domain exceptions to HTTP status codes:

```python
from fastapi import HTTPException
from app.context.auth.domain.exceptions import (
    InvalidCredentialsError,
    AccountLockedError,
)

@router.post("/login")
async def login(request: LoginRequest):
    try:
        result = await handler.handle(...)
        return result
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except AccountLockedError as e:
        raise HTTPException(status_code=403, detail=str(e))
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

## Module Initialization Pattern

**All `__init__.py` files** must follow this pattern to provide a clean, refactorable public API.

### Pattern

```python
# app/context/user_account/domain/value_objects/__init__.py
from .account_id import AccountID
from .account_name import AccountName
from .balance import Balance
from .currency import Currency

__all__ = ["AccountName", "AccountID", "Balance", "Currency"]
```

### Rules

1. Use **relative imports** (`.module_name`) to import from individual files within the package
2. Define an explicit **`__all__` list** to declare the public API
3. **Always import from the module directory**, never from individual files

### Usage

```python
# Good - import from module
from app.context.user_account.domain.value_objects import AccountID, Balance

# Bad - import directly from file
from app.context.user_account.domain.value_objects.account_id import AccountID
```

### Benefits

- **Cleaner imports** - Shorter, more readable import statements
- **Easier refactoring** - Internal file structure can change without breaking imports
- **Explicit public API** - `__all__` makes it clear what's meant to be used externally
- **Consistency** - Same pattern across the entire codebase

### Where to Apply

Apply this pattern to **all directories** containing multiple Python modules:

- `value_objects/`
- `dto/`
- `contracts/`
- `services/`
- `handlers/`
- `commands/`
- `queries/`
- `repositories/`
- `mappers/`
- `schemas/`
- Any other package with multiple modules

## Commands and Queries (CQRS)

### Use Primitives Only

Commands and queries should **only use primitive types** (str, int, float, bool, etc.). They should NOT use value objects or domain types.

**Rationale:**
- Commands/queries are application-layer DTOs for transferring data from controllers to handlers
- Value object validation and construction happens in the handler, not at the boundary
- Keeps commands/queries simple and framework-agnostic
- Allows handlers to control when and how validation occurs

```python
# Good - uses primitives
@dataclass(frozen=True)
class LoginCommand:
    email: str
    password: str

# Bad - uses value objects
@dataclass(frozen=True)
class LoginCommand:
    email: Email  # Don't do this!
    password: Password  # Don't do this!
```

**Handler converts primitives to value objects:**

```python
class LoginHandler:
    async def handle(self, command: LoginCommand) -> LoginResult:
        # Handler constructs value objects from primitives
        email = SharedEmail(command.email)  # Validation happens here
        password = SharedPassword.from_plain_text(command.password)

        # Now use value objects with domain service
        result = await self._login_service.login(email, password)
        return result
```

**Complete data flow:**

```
Controller (Pydantic model with primitives)
    ↓
Command/Query (primitives)
    ↓
Handler (converts to value objects)
    ↓
Domain Service (uses value objects)
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
