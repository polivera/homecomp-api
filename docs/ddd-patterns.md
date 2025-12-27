# DDD & CQRS Implementation Patterns

This document provides comprehensive guidance on implementing Domain-Driven Design (DDD) and Command Query Responsibility Segregation (CQRS) patterns in this codebase.

## Table of Contents

- [When to Use Commands vs Queries](#when-to-use-commands-vs-queries)
- [Command Data Flow](#command-data-flow)
- [Query Data Flow](#query-data-flow)
- [Interface Definitions (Contracts)](#interface-definitions-contracts)
- [Dependency Injection Setup](#dependency-injection-setup)
- [Commands and Queries Structure](#commands-and-queries-structure)
- [Complete Layer Communication Summary](#complete-layer-communication-summary)

---

## When to Use Commands vs Queries

### Use a Command When

The operation **modifies state** (creates, updates, deletes):
- Business rules or validations are required
- Domain services need to be invoked
- Side effects occur (database writes, external API calls, events)

**Examples:**
- `LoginCommand` - Creates a session/token
- `RegisterUserCommand` - Creates a new user
- `UpdateProfileCommand` - Modifies user data
- `DeleteAccountCommand` - Removes user data

### Use a Query When

The operation **only reads data** (no side effects):
- No business logic is needed, just data retrieval
- You're fetching data for display or decision-making
- No state changes occur

**Examples:**
- `FindUserQuery` - Retrieves user by ID
- `GetUserProfileQuery` - Gets user profile data
- `ListUsersQuery` - Returns list of users
- `SearchEntriesQuery` - Searches for entries

### Golden Rule

**If it changes state → Command**
**If it only reads → Query**

---

## Command Data Flow

Commands flow through the system to execute business logic and modify state.

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ COMMAND FLOW (Write Operations)                                 │
└─────────────────────────────────────────────────────────────────┘

1. Interface Layer (REST Controller)
   ├─ Receives HTTP request
   ├─ Validates with Pydantic schema (request)
   └─ Creates Command object
         ↓
2. Application Layer (Command Handler)
   ├─ Receives Command
   ├─ Calls Domain Service (business logic)
   └─ Returns Application DTO
         ↓
3. Domain Layer (Domain Service)
   ├─ Executes business rules
   ├─ Validates using Value Objects
   ├─ Calls Repository Contract (interface)
   └─ Returns Domain DTO
         ↓
4. Infrastructure Layer (Repository)
   ├─ Receives domain data
   ├─ Performs database operations
   ├─ Maps SQLAlchemy models ↔ Domain DTOs
   └─ Returns Domain DTO to service
         ↓
5. Back to Controller
   └─ Converts Application DTO → Frozen Dataclass (response)
```

### Example: Login Command Flow

#### 1. Interface Layer (Controller)

```python
# File: app/context/auth/interface/rest/controllers/login_controller.py

@router.post("/login")
async def login(
    request: LoginRequest,  # Pydantic (validation)
    handler: LoginHandlerContract = Depends(get_login_handler),
) -> LoginResponse:  # Frozen dataclass (performance)
    # Create command from request
    command = LoginCommand(
        email=SharedEmail(request.email),
        password=SharedPassword.from_plain_text(request.password),
    )

    # Execute via handler
    result = await handler.handle(command)

    # Return frozen dataclass response
    return LoginResponse(
        message=result.message,
        token=result.token,
    )
```

#### 2. Application Layer (Command Handler)

```python
# File: app/context/auth/application/handlers/login_handler.py

class LoginHandler(LoginHandlerContract):
    def __init__(self, login_service: LoginServiceContract):
        self._login_service = login_service

    async def handle(self, command: LoginCommand) -> LoginDTO:
        # Delegate to domain service (business logic)
        return await self._login_service.authenticate(
            email=command.email,
            password=command.password,
        )
```

#### 3. Domain Layer (Domain Service)

```python
# File: app/context/auth/domain/services/login_service.py

class LoginService(LoginServiceContract):
    def __init__(self, user_repository: UserRepositoryContract):
        self._user_repository = user_repository

    async def authenticate(
        self,
        email: SharedEmail,
        password: SharedPassword,
    ) -> LoginDTO:
        # Business logic: find user
        user = await self._user_repository.find_user(email=email)

        if not user:
            raise ValueError("Invalid credentials")

        # Business logic: verify password
        if not user.password.verify(password.value):
            raise ValueError("Invalid credentials")

        # Business logic: generate token (example)
        token = self._generate_token(user.user_id)

        # Return domain result
        return LoginDTO(
            user_id=user.user_id,
            email=user.email,
            message="Login successful",
            token=token,
        )

    def _generate_token(self, user_id: UserID) -> str:
        # Token generation logic here
        pass
```

#### 4. Infrastructure Layer (Repository)

```python
# File: app/context/user/infrastructure/repositories/user_repository.py

class UserRepository(UserRepositoryContract):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def find_user(
        self,
        email: Optional[SharedEmail] = None,
    ) -> Optional[UserDTO]:
        # Database query
        query = select(UserModel).where(UserModel.email == email.value)
        result = await self._db.execute(query)
        model = result.scalar_one_or_none()

        # Map to domain DTO
        return UserMapper.toDTO(model) if model else None
```

---

## Query Data Flow

Queries bypass the domain layer and go directly to infrastructure for optimized read operations.

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ QUERY FLOW (Read Operations)                                    │
└─────────────────────────────────────────────────────────────────┘

1. Interface Layer (REST Controller)
   ├─ Receives HTTP request
   ├─ Validates path/query parameters
   └─ Creates Query object
         ↓
2. Application Layer (Query Handler)
   ├─ Receives Query
   ├─ Calls Repository Contract directly (NO domain service)
   └─ Returns Application DTO
         ↓
3. Infrastructure Layer (Repository)
   ├─ Performs database read
   ├─ Maps SQLAlchemy model → Domain DTO
   └─ Returns Domain DTO to handler
         ↓
4. Back to Controller
   └─ Converts Application DTO → Frozen Dataclass (response)
```

### Key Difference

**Queries skip the domain layer** because they don't need business logic - they're pure data retrieval.

### Example: Find User Query Flow

#### 1. Interface Layer (Controller)

```python
# File: app/context/user/interface/rest/controllers/user_controller.py

@router.get("/users/{user_id}")
async def get_user(
    user_id: str,
    handler: FindUserHandlerContract = Depends(get_find_user_handler),
) -> UserResponse:  # Frozen dataclass
    # Create query
    query = FindUserQuery(user_id=UserID(user_id))

    # Execute via handler
    result = await handler.handle(query)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    # Return frozen dataclass response
    return UserResponse(
        user_id=result.user_id.value,
        email=result.email.value,
        created_at=result.created_at,
    )
```

#### 2. Application Layer (Query Handler)

```python
# File: app/context/user/application/handlers/find_user_handler.py

class FindUserHandler(FindUserHandlerContract):
    def __init__(self, repository: UserRepositoryContract):
        self._repository = repository

    async def handle(self, query: FindUserQuery) -> Optional[UserDTO]:
        # Call repository directly (no domain service needed)
        return await self._repository.find_user(user_id=query.user_id)
```

#### 3. Infrastructure Layer (Repository)

```python
# File: app/context/user/infrastructure/repositories/user_repository.py

class UserRepository(UserRepositoryContract):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def find_user(
        self,
        user_id: Optional[UserID] = None,
    ) -> Optional[UserDTO]:
        # Database query
        query = select(UserModel).where(UserModel.id == user_id.value)
        result = await self._db.execute(query)
        model = result.scalar_one_or_none()

        # Map to domain DTO
        return UserMapper.toDTO(model) if model else None
```

---

## Interface Definitions (Contracts)

All components are accessed via **contracts** (abstract base classes) to enable dependency injection and testability.

### Why Contracts?

1. **Dependency Inversion Principle** - High-level modules don't depend on low-level modules
2. **Testability** - Easy to mock for unit tests
3. **Flexibility** - Swap implementations without changing consumers
4. **Clear Interfaces** - Explicit contract between layers

### Contract Types and Locations

#### Domain Service Contract

Located in `domain/contracts/{service}_contract.py`

```python
# File: app/context/auth/domain/contracts/login_service_contract.py

from abc import ABC, abstractmethod
from app.shared.domain.value_objects.shared_email import SharedEmail
from app.shared.domain.value_objects.shared_password import SharedPassword
from app.context.auth.domain.dto.login_dto import LoginDTO


class LoginServiceContract(ABC):
    """Contract for login domain service."""

    @abstractmethod
    async def authenticate(
        self,
        email: SharedEmail,
        password: SharedPassword,
    ) -> LoginDTO:
        """
        Authenticate user with email and password.

        Args:
            email: User's email address
            password: User's password (plain text)

        Returns:
            LoginDTO with user info and token

        Raises:
            ValueError: If credentials are invalid
        """
        pass
```

#### Handler Contract

Located in `application/contracts/{handler}_contract.py`

```python
# File: app/context/auth/application/contracts/login_handler_contract.py

from abc import ABC, abstractmethod
from app.context.auth.application.commands.login_command import LoginCommand
from app.context.auth.application.dto.login_dto import LoginDTO


class LoginHandlerContract(ABC):
    """Contract for login command handler."""

    @abstractmethod
    async def handle(self, command: LoginCommand) -> LoginDTO:
        """
        Handle login command.

        Args:
            command: Login command with credentials

        Returns:
            LoginDTO with result
        """
        pass
```

#### Repository Contract

Located in `domain/contracts/{repository}_contract.py`

```python
# File: app/context/user/domain/contracts/user_repository_contract.py

from abc import ABC, abstractmethod
from typing import Optional
from app.shared.domain.value_objects.shared_email import SharedEmail
from app.context.user.domain.value_objects.user_id import UserID
from app.context.user.domain.dto.user_dto import UserDTO


class UserRepositoryContract(ABC):
    """Contract for user repository."""

    @abstractmethod
    async def find_user(
        self,
        user_id: Optional[UserID] = None,
        email: Optional[SharedEmail] = None,
    ) -> Optional[UserDTO]:
        """
        Find user by ID or email.

        Args:
            user_id: User ID to search for
            email: Email to search for

        Returns:
            UserDTO if found, None otherwise
        """
        pass

    @abstractmethod
    async def create_user(self, user: UserDTO) -> UserDTO:
        """
        Create new user.

        Args:
            user: User data to create

        Returns:
            Created user DTO
        """
        pass
```

### Contract Placement Rules

| Contract Type | Location | Reason |
|--------------|----------|--------|
| **Domain Service Contract** | `domain/contracts/` | Domain defines its own interfaces |
| **Repository Contract** | `domain/contracts/` | Domain defines data needs (Dependency Inversion) |
| **Handler Contract** | `application/contracts/` | Application layer owns handlers |

### Why Repositories in Domain Contracts?

This follows the **Dependency Inversion Principle**:
- Domain layer defines **what data it needs** (the interface)
- Infrastructure layer provides **how to get it** (the implementation)
- Domain never depends on infrastructure

---

## Dependency Injection Setup

All dependencies are wired in `infrastructure/dependencies.py` using FastAPI's `Depends()` mechanism.

### Dependency Chain

Dependencies are built **bottom-up** (from infrastructure to interface):

```
get_db (shared infrastructure)
   ↓
get_repository (infrastructure)
   ↓
get_domain_service (domain)
   ↓
get_handler (application)
   ↓
controller (interface)
```

### Complete Example: Auth Context Dependencies

```python
# File: app/context/auth/infrastructure/dependencies.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.infrastructure.database import get_db

# Cross-context dependency (from User context)
from app.context.user.application.contracts.find_user_handler_contract import (
    FindUserHandlerContract,
)
from app.context.user.infrastructure.dependencies import get_find_user_handler

from app.context.auth.domain.contracts.login_service_contract import (
    LoginServiceContract,
)
from app.context.auth.domain.services.login_service import LoginService
from app.context.auth.application.contracts.login_handler_contract import (
    LoginHandlerContract,
)
from app.context.auth.application.handlers.login_handler import LoginHandler


# ─────────────────────────────────────────────────────────────────
# DOMAIN SERVICE LAYER
# ─────────────────────────────────────────────────────────────────

def get_login_service(
    # Inject handler from another context (cross-context communication)
    find_user_handler: FindUserHandlerContract = Depends(get_find_user_handler),
) -> LoginServiceContract:
    """
    Inject login domain service.

    Returns:
        LoginServiceContract implementation
    """
    return LoginService(find_user_handler)


# ─────────────────────────────────────────────────────────────────
# APPLICATION HANDLER LAYER
# ─────────────────────────────────────────────────────────────────

def get_login_handler(
    login_service: LoginServiceContract = Depends(get_login_service),
) -> LoginHandlerContract:
    """
    Inject login command handler.

    Returns:
        LoginHandlerContract implementation
    """
    return LoginHandler(login_service)
```

### User Context Dependencies

```python
# File: app/context/user/infrastructure/dependencies.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.infrastructure.database import get_db

from app.context.user.domain.contracts.user_repository_contract import (
    UserRepositoryContract,
)
from app.context.user.infrastructure.repositories.user_repository import (
    UserRepository,
)
from app.context.user.application.contracts.find_user_handler_contract import (
    FindUserHandlerContract,
)
from app.context.user.application.handlers.find_user_handler import FindUserHandler


# ─────────────────────────────────────────────────────────────────
# REPOSITORY LAYER
# ─────────────────────────────────────────────────────────────────

def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepositoryContract:
    """
    Inject user repository.

    Args:
        db: Database session from shared infrastructure

    Returns:
        UserRepositoryContract implementation
    """
    return UserRepository(db)


# ─────────────────────────────────────────────────────────────────
# APPLICATION HANDLER LAYER
# ─────────────────────────────────────────────────────────────────

def get_find_user_handler(
    repository: UserRepositoryContract = Depends(get_user_repository),
) -> FindUserHandlerContract:
    """
    Inject find user query handler.

    Returns:
        FindUserHandlerContract implementation
    """
    return FindUserHandler(repository)
```

### Dependency Injection Rules

#### 1. Always Inject Contracts, Never Implementations

```python
# ✅ CORRECT - Inject contract
def get_handler(
    service: ServiceContract = Depends(get_service),
) -> HandlerContract:
    return Handler(service)

# ❌ WRONG - Inject concrete implementation
def get_handler(
    service: ConcreteService = Depends(get_service),
) -> HandlerContract:
    return Handler(service)
```

#### 2. Database Sessions Come from Shared Infrastructure

```python
# ✅ CORRECT
from app.shared.infrastructure.database import get_db

def get_repository(
    db: AsyncSession = Depends(get_db),
) -> RepositoryContract:
    return Repository(db)
```

#### 3. Cross-Context Dependencies Use Handler Contracts

When one context needs data from another context:

```python
# ✅ CORRECT - Auth context uses User context via handler contract
from app.context.user.application.contracts.find_user_handler_contract import (
    FindUserHandlerContract,
)
from app.context.user.infrastructure.dependencies import get_find_user_handler

def get_auth_service(
    user_handler: FindUserHandlerContract = Depends(get_find_user_handler),
) -> AuthServiceContract:
    return AuthService(user_handler)
```

```python
# ❌ WRONG - Never access repositories directly across contexts
from app.context.user.infrastructure.repositories.user_repository import UserRepository

def get_auth_service(
    user_repo: UserRepository = Depends(...),  # WRONG!
):
    return AuthService(user_repo)
```

#### 4. Return Type Must Match Contract

```python
# ✅ CORRECT
def get_service() -> ServiceContract:
    return ConcreteService()  # ConcreteService implements ServiceContract

# ❌ WRONG
def get_service() -> ConcreteService:  # Should return contract type
    return ConcreteService()
```

---

## Commands and Queries Structure

### Command Structure

Commands are immutable data containers representing write operations.

```python
# File: app/context/{context}/application/commands/{action}_command.py

from dataclasses import dataclass
from app.shared.domain.value_objects.shared_email import SharedEmail
from app.shared.domain.value_objects.shared_password import SharedPassword


@dataclass(frozen=True)
class LoginCommand:
    """
    Command to authenticate a user.

    Attributes:
        email: User's email address
        password: User's password (plain text, will be hashed)
    """
    email: SharedEmail
    password: SharedPassword
```

### Query Structure

Queries are immutable data containers representing read operations.

```python
# File: app/context/{context}/application/queries/{action}_query.py

from dataclasses import dataclass
from typing import Optional
from app.context.user.domain.value_objects.user_id import UserID
from app.shared.domain.value_objects.shared_email import SharedEmail


@dataclass(frozen=True)
class FindUserQuery:
    """
    Query to find a user by ID or email.

    Attributes:
        user_id: User ID to search for (optional)
        email: Email to search for (optional)
    """
    user_id: Optional[UserID] = None
    email: Optional[SharedEmail] = None
```

### Key Characteristics

| Aspect | Commands | Queries |
|--------|----------|---------|
| **Mutability** | Frozen (`frozen=True`) | Frozen (`frozen=True`) |
| **Purpose** | Represent write operations | Represent read operations |
| **Fields** | Usually **required** | Often **optional** (for filtering) |
| **Types** | Use Value Objects | Use Value Objects |
| **Logic** | No logic, just data | No logic, just data |

### Best Practices

1. **Always use Value Objects, not primitives**
   ```python
   # ✅ CORRECT
   @dataclass(frozen=True)
   class CreateUserCommand:
       email: SharedEmail
       password: SharedPassword

   # ❌ WRONG
   @dataclass(frozen=True)
   class CreateUserCommand:
       email: str  # Should be SharedEmail
       password: str  # Should be SharedPassword
   ```

2. **Make them immutable with `frozen=True`**
   ```python
   # ✅ CORRECT
   @dataclass(frozen=True)
   class UpdateProfileCommand:
       user_id: UserID
       name: str

   # ❌ WRONG
   @dataclass  # Missing frozen=True
   class UpdateProfileCommand:
       user_id: UserID
       name: str
   ```

3. **Keep them simple - no methods or logic**
   ```python
   # ✅ CORRECT
   @dataclass(frozen=True)
   class LoginCommand:
       email: SharedEmail
       password: SharedPassword

   # ❌ WRONG
   @dataclass(frozen=True)
   class LoginCommand:
       email: SharedEmail
       password: SharedPassword

       def validate(self):  # NO LOGIC IN COMMANDS!
           if not self.email:
               raise ValueError("Email required")
   ```

---

## Complete Layer Communication Summary

### Visual Layer Communication

```
┌──────────────────────────────────────────────────────────────────┐
│ LAYER COMMUNICATION RULES                                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ INTERFACE LAYER (REST Controllers)                              │
│   ├─ Depends on: Application Handlers (via contracts)           │
│   ├─ Receives: Pydantic schemas (request validation)            │
│   ├─ Creates: Commands/Queries                                  │
│   └─ Returns: Frozen dataclasses (response)                     │
│                                                                  │
│                          ↓                                       │
│                                                                  │
│ APPLICATION LAYER (Handlers)                                    │
│   ├─ Depends on: Domain Services (Commands) OR                  │
│   │              Repositories (Queries)                         │
│   ├─ Receives: Commands/Queries                                 │
│   ├─ Orchestrates: Domain services or repository calls          │
│   └─ Returns: Application DTOs                                  │
│                                                                  │
│                          ↓                                       │
│                                                                  │
│ DOMAIN LAYER (Services)                                         │
│   ├─ Depends on: Repository Contracts ONLY                      │
│   ├─ Contains: Business logic and rules                         │
│   ├─ Uses: Value Objects, Domain DTOs                           │
│   └─ Returns: Domain DTOs                                       │
│                                                                  │
│                          ↓                                       │
│                                                                  │
│ INFRASTRUCTURE LAYER (Repositories)                             │
│   ├─ Depends on: Database session                               │
│   ├─ Implements: Repository Contracts                           │
│   ├─ Uses: SQLAlchemy models, Mappers                           │
│   └─ Returns: Domain DTOs                                       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Dependency Flow Rules

**CRITICAL RULE**: Dependencies only flow **INWARD** and **DOWNWARD**

```
         ┌─────────────┐
         │  Interface  │ (depends on Application)
         └──────┬──────┘
                │
                ↓
         ┌─────────────┐
         │ Application │ (depends on Domain)
         └──────┬──────┘
                │
                ↓
         ┌─────────────┐
         │   Domain    │ (depends on NOTHING)
         └──────┬──────┘
                ↑
                │ (implements contracts)
                │
         ┌─────────────┐
         │Infrastructure│
         └─────────────┘
```

### Layer Responsibilities

#### Interface Layer
- **Concerns**: HTTP, REST, serialization
- **Depends on**: Application handlers (contracts)
- **Returns**: Frozen dataclasses for responses
- **Never**: Contains business logic

#### Application Layer
- **Concerns**: Use case orchestration
- **Depends on**: Domain services (commands) or repositories (queries)
- **Coordinates**: Multiple domain services if needed
- **Never**: Contains business logic

#### Domain Layer
- **Concerns**: Business rules and logic
- **Depends on**: Repository contracts only
- **Contains**: All business validation and rules
- **Never**: Depends on outer layers

#### Infrastructure Layer
- **Concerns**: External systems (database, APIs, file system)
- **Implements**: Domain contracts
- **Uses**: Mappers to convert between models and DTOs
- **Never**: Contains business logic

### Cross-Context Communication

When Context A needs data from Context B:

```python
# ✅ CORRECT - Use handler contracts
# Auth context needs User data

# 1. Import handler contract from User context
from app.context.user.application.contracts.find_user_handler_contract import (
    FindUserHandlerContract,
)

# 2. Import dependency function
from app.context.user.infrastructure.dependencies import get_find_user_handler

# 3. Inject in Auth context
def get_login_service(
    find_user_handler: FindUserHandlerContract = Depends(get_find_user_handler),
) -> LoginServiceContract:
    return LoginService(find_user_handler)
```

```python
# ❌ WRONG - Never access repositories directly
from app.context.user.infrastructure.repositories.user_repository import UserRepository

def get_login_service(
    user_repo: UserRepository = Depends(...),  # WRONG!
):
    return LoginService(user_repo)
```

### Common Anti-Patterns to Avoid

#### 1. Domain Depending on Infrastructure

```python
# ❌ WRONG
# File: domain/services/user_service.py
from app.context.user.infrastructure.models.user_model import UserModel  # WRONG!

class UserService:
    def create_user(self, model: UserModel):  # WRONG!
        pass
```

```python
# ✅ CORRECT
# File: domain/services/user_service.py
from app.context.user.domain.dto.user_dto import UserDTO

class UserService:
    def create_user(self, user: UserDTO):
        pass
```

#### 2. Putting Business Logic in Controllers

```python
# ❌ WRONG
@router.post("/login")
async def login(request: LoginRequest):
    # Business logic in controller - WRONG!
    user = await db.execute(select(UserModel)...)
    if not user:
        raise HTTPException(400)
    if not verify_password(request.password, user.password):
        raise HTTPException(400)
    return {"token": generate_token(user.id)}
```

```python
# ✅ CORRECT
@router.post("/login")
async def login(
    request: LoginRequest,
    handler: LoginHandlerContract = Depends(get_login_handler),
):
    command = LoginCommand(email=request.email, password=request.password)
    result = await handler.handle(command)
    return LoginResponse(token=result.token)
```

#### 3. Skipping the Handler Layer

```python
# ❌ WRONG
@router.post("/users")
async def create_user(
    request: CreateUserRequest,
    service: UserServiceContract = Depends(get_user_service),  # WRONG!
):
    # Controller calling service directly - skip handler
    result = await service.create_user(...)
```

```python
# ✅ CORRECT
@router.post("/users")
async def create_user(
    request: CreateUserRequest,
    handler: CreateUserHandlerContract = Depends(get_create_user_handler),
):
    command = CreateUserCommand(...)
    result = await handler.handle(command)
    return UserResponse(...)
```

---

## Summary Checklist

When implementing new features, ensure:

- [ ] **Commands** for state changes, **Queries** for reads
- [ ] **Commands** flow: Interface → Handler → Domain Service → Repository
- [ ] **Queries** flow: Interface → Handler → Repository (skip domain)
- [ ] All components accessed via **contracts** (interfaces)
- [ ] Dependencies defined in `infrastructure/dependencies.py`
- [ ] Always inject **contracts**, never implementations
- [ ] Cross-context communication via **handler contracts**
- [ ] Domain layer has **no dependencies** on outer layers
- [ ] Business logic **only** in domain services
- [ ] Controllers return **frozen dataclasses** for responses
- [ ] Use **Value Objects** instead of primitives
- [ ] Repository contracts in **domain/contracts**
- [ ] Infrastructure **implements** domain contracts

---

**Remember**: The goal of DDD and CQRS is to create a maintainable, testable, and flexible codebase by clearly separating concerns and enforcing dependency rules. When in doubt, ask: "Does this violate the dependency rule?" and "Is business logic where it belongs (domain layer)?"
