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

### Context-Specific Value Objects

**Rule:** To maintain bounded context isolation, **always create context-specific value objects** by extending shared value objects. Never use shared value objects directly in domain models or DTOs.

**Pattern:**

```python
# Shared Kernel - validation logic
# app/shared/domain/value_objects/shared_currency.py
@dataclass(frozen=True)
class SharedCurrency:
    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            # Validation logic
            if len(self.value) != 3:
                raise ValueError("Currency must be 3 characters")

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        return cls(value, _validated=True)

# Context-specific wrapper
# app/context/user_account/domain/value_objects/account_currency.py
@dataclass(frozen=True)
class UserAccountCurrency(SharedCurrency):
    pass  # Inherits all validation from SharedCurrency

# Another context-specific wrapper
# app/context/credit_card/domain/value_objects/credit_card_currency.py
@dataclass(frozen=True)
class CreditCardCurrency(SharedCurrency):
    pass  # Can add context-specific behavior later if needed
```

**Usage in Domain Models:**

```python
# Good - uses context-specific type
@dataclass(frozen=True)
class UserAccountDTO:
    account_id: AccountID
    currency: UserAccountCurrency  # ✅ Context-specific

# Bad - uses shared type directly
@dataclass(frozen=True)
class UserAccountDTO:
    account_id: AccountID
    currency: SharedCurrency  # ❌ Breaks context isolation

# Bad - uses wrong context's type
@dataclass(frozen=True)
class UserAccountDTO:
    account_id: AccountID
    currency: CreditCardCurrency  # ❌ Cross-context dependency
```

**Rationale:**
- Maintains strict bounded context boundaries
- Prevents accidental cross-context dependencies
- Allows future context-specific behavior without breaking changes
- Makes code explicitly show which context owns the value
- Type system enforces architectural boundaries

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

## Application Layer Handlers

### Exception Handling and Result Pattern

**Rule:** Handlers MUST catch all domain exceptions and convert them to Result objects. Handlers should NEVER let exceptions propagate to the controller layer.

**Rationale:**
- Keeps handlers HTTP-agnostic and framework-independent
- Makes handlers easier to test (no exception handling needed in tests)
- Centralizes error-to-message mapping in the handler
- Controllers can map error codes to HTTP status codes programmatically (no string parsing!)

### Result DTO Pattern with Error Codes

All handler result DTOs should follow this pattern:

```python
# app/context/user_account/application/dto/create_account_result.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class CreateAccountErrorCode(str, Enum):
    """Error codes for account creation"""
    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"

@dataclass(frozen=True)
class CreateAccountResult:
    """Result of account creation operation"""

    # Success fields - populated when operation succeeds
    account_id: Optional[int] = None
    account_name: Optional[str] = None
    account_balance: Optional[float] = None

    # Error fields - populated when operation fails
    error_code: Optional[CreateAccountErrorCode] = None
    error_message: Optional[str] = None
```

**Pattern rules:**
- Define a context-specific error code enum (inheriting from `str, Enum`)
- Use `Optional` for all fields
- Success data fields default to `None`
- Include both `error_code` and `error_message` fields
- On success: populate data fields, leave error fields as None
- On failure: populate both error_code (for logic) and error_message (for users)

### Handler Implementation Pattern

**All handlers MUST follow this exception handling pattern:**

```python
class CreateAccountHandler(CreateAccountHandlerContract):
    """Handler for create account command"""

    def __init__(self, service: CreateAccountServiceContract):
        self._service = service

    async def handle(self, command: CreateAccountCommand) -> CreateAccountResult:
        """Execute the create account command"""

        try:
            # 1. Convert command primitives to value objects
            account_dto = await self._service.create_account(
                user_id=UserAccountUserID(command.user_id),
                name=AccountName(command.name),
                currency=UserAccountCurrency(command.currency),
                balance=UserAccountBalance.from_float(command.balance),
            )

            # 2. Validate operation succeeded
            if account_dto.account_id is None:
                return CreateAccountResult(
                    error_code=CreateAccountErrorCode.UNEXPECTED_ERROR,
                    error_message="Error creating account",
                )

            # 3. Convert domain DTO to result with primitives
            return CreateAccountResult(
                account_id=account_dto.account_id.value,
                account_name=account_dto.name.value,
                account_balance=float(account_dto.balance.value),
            )

        # 4. Catch specific domain exceptions and return error code + message
        except UserAccountNameAlreadyExistError:
            return CreateAccountResult(
                error_code=CreateAccountErrorCode.NAME_ALREADY_EXISTS,
                error_message="Account name already exist",
            )
        except UserAccountMapperError:
            return CreateAccountResult(
                error_code=CreateAccountErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to dto",
            )

        # 5. Always catch generic Exception as final fallback
        except Exception:
            return CreateAccountResult(
                error_code=CreateAccountErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
```

**Handler Exception Handling Rules:**

1. **Wrap entire handler logic in try/except**
2. **Catch specific domain exceptions first** - Map each to error code + user-friendly message
3. **Always catch `Exception` as final fallback** - Prevents any exception from escaping the handler
4. **Return Result object with error_code and error_message** - Never re-raise exceptions
5. **Use user-friendly error messages** - These go directly to the API response

**Exception Ordering:**

```python
try:
    # Handler logic
    pass
except SpecificDomainException1:  # Most specific first
    return Result(
        error_code=ErrorCode.SPECIFIC_ERROR_1,
        error_message="Specific error message 1",
    )
except SpecificDomainException2:
    return Result(
        error_code=ErrorCode.SPECIFIC_ERROR_2,
        error_message="Specific error message 2",
    )
except Exception:  # Generic catch-all last
    return Result(
        error_code=ErrorCode.UNEXPECTED_ERROR,
        error_message="Unexpected error",
    )
```

### Controller Integration with Error Codes

Controllers check the result.error_code field and map to HTTP status codes:

```python
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

@router.post("/accounts", status_code=201)
async def create_account(
    request: CreateAccountRequest,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Create a new user account"""
    handler = app_container.get_create_account_handler()

    command = CreateAccountCommand(
        user_id=user_id,
        name=request.name,
        currency=request.currency,
        balance=request.balance,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        # Map error codes to status codes (no string parsing!)
        status_code_map = {
            CreateAccountErrorCode.NAME_ALREADY_EXISTS: 409,  # Conflict
            CreateAccountErrorCode.MAPPER_ERROR: 500,  # Internal Server Error
            CreateAccountErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }

        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return success response
    return CreateAccountResponse(
        id=result.account_id,
        name=result.account_name,
        balance=result.account_balance,
    )
```

**Benefits of Error Code Pattern:**

- **Type Safety**: Error codes are enums, preventing typos
- **No String Parsing**: Controllers use error codes for logic, not string matching
- **Refactor-Friendly**: Can change error messages without breaking controller logic
- **Explicit Mapping**: Clear mapping between domain errors and HTTP status codes
- **IDE Support**: Autocomplete and type checking for error codes
- **Documentation**: Error codes serve as documentation of possible failures

## Dependency Injection

**IMPORTANT**: This project uses the **ApplicationContainer** pattern for centralized dependency management.

### Define Factory Functions in Infrastructure Layer

Factory functions take `db: AsyncSession` and `logger: LoggerContract` as parameters and return fully configured handlers:

```python
# infrastructure/dependencies/dependencies.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.domain.contracts import LoggerContract

def login_handler_factory(db: AsyncSession, logger: LoggerContract) -> LoginHandlerContract:
    """Factory for LoginHandler with all dependencies"""
    from app.context.auth.infrastructure.repositories import SessionRepository
    from app.context.auth.domain.services import LoginService
    from app.context.auth.application.handlers import LoginHandler

    # Private helper to get repository
    session_repo = _get_session_repository(db)
    # Private helper to get service
    login_service = _get_login_service(session_repo, logger)

    return LoginHandler(login_service, logger)

def _get_session_repository(db: AsyncSession) -> SessionRepositoryContract:
    """Private helper to get repository instance"""
    from app.context.auth.infrastructure.repositories import SessionRepository
    return SessionRepository(db)

def _get_login_service(
    session_repo: SessionRepositoryContract,
    logger: LoggerContract,
) -> LoginServiceContract:
    """Private helper to get service instance"""
    from app.context.auth.domain.services import LoginService
    return LoginService(session_repo, logger)
```

**Export factories in `__init__.py`:**

```python
# infrastructure/dependencies/__init__.py
from .dependencies import login_handler_factory

__all__ = ["login_handler_factory"]
```

### Register Factories in ApplicationContainer

Add handler getter methods to the ApplicationContainer:

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

### Use ApplicationContainer in Controllers

Controllers inject the ApplicationContainer and access dependencies through it:

```python
from typing import Annotated
from fastapi import APIRouter, Depends
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container

@router.post("/login")
async def login(
    request: LoginRequest,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
):
    # Get dependencies from container
    logger = app_container.logger
    handler = app_container.get_login_handler()

    # Use handler
    command = LoginCommand(...)
    result = await handler.handle(command)
    return result
```

**Benefits of this pattern:**
- **Centralized dependency management** - All wiring happens in one place (ApplicationContainer)
- **Cleaner controllers** - Single container injection instead of multiple `Depends()`
- **Easier testing** - Mock the entire container instead of individual dependencies
- **Consistent across contexts** - Same pattern for all bounded contexts
- **Better separation of concerns** - Dependency wiring separated from business logic

### Authenticating Requests

**Rule:** Always inject the authenticated user ID using the shared middleware dependency. Pass user_id as a **primitive** (int) to commands/queries.

**Pattern:**

```python
from typing import Annotated
from fastapi import APIRouter, Depends
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

@router.post("/accounts", status_code=201)
async def create_account(
    request: CreateAccountRequest,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],  # ✅ Inject authenticated user
):
    """Create a new user account"""
    # Get dependencies from container
    logger = app_container.logger
    handler = app_container.get_create_account_handler()

    command = CreateAccountCommand(
        user_id=user_id,  # ✅ Pass primitive to command
        name=request.name,
        currency=request.currency,
        balance=request.balance,
    )
    result = await handler.handle(command)
    return result
```

**Available Middleware Functions:**

```python
# Required authentication - raises 401 if missing/invalid
from app.shared.infrastructure.middleware import get_current_user_id

async def protected_route(user_id: int = Depends(get_current_user_id)):
    # user_id is always present, or 401 was raised
    pass

# Optional authentication - returns None if not authenticated
from app.shared.infrastructure.middleware import get_current_user_id_optional

async def public_route(user_id: Optional[int] = Depends(get_current_user_id_optional)):
    # user_id might be None (for personalized public content)
    if user_id:
        # Show personalized content
        pass
    else:
        # Show default content
        pass
```

**Command includes user_id as primitive:**

```python
@dataclass(frozen=True)
class CreateAccountCommand:
    user_id: int  # ✅ Primitive (consistent with CQRS pattern)
    name: str
    currency: str
    balance: float
```

**Handler converts to value object:**

```python
class CreateAccountHandler:
    async def handle(self, command: CreateAccountCommand) -> CreateAccountResult:
        # Convert primitive to value object
        user_id = UserID(command.user_id)  # ✅ Handler responsibility

        # Use value object in domain layer
        result = await self._service.create_account(user_id=user_id, ...)
        return result
```

**Important:**
- Never manually extract tokens or validate sessions in controllers
- Never pass `UserID` value objects in commands/queries
- Middleware handles all authentication logic (extraction, validation, session lookup)
- Controllers receive clean primitive `int` user_id
- Handlers convert primitives to value objects for domain layer

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
