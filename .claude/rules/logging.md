# Logging Guidelines

## Overview

This application uses **structlog** for structured logging with automatic routing to different backends based on environment:
- **Development** (`APP_ENV=dev`): Console (colored) + Loki (structured JSON)
- **Test** (`APP_ENV=test`): NullLogger (no output)
- **Production** (`APP_ENV=production`): Console (JSON) → Docker logs → Promtail → Loki

## Core Principles

### 1. Always Use Dependency Injection

**NEVER** instantiate loggers directly. Always inject via `get_logger()` dependency.

```python
# Good - dependency injection
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger

class LoginHandler:
    def __init__(self, logger: LoggerContract):
        self._logger = logger

# Bad - direct instantiation
import structlog
logger = structlog.get_logger()  # Don't do this!
```

### 2. Logger is Environment-Aware

The `get_logger()` factory automatically returns:
- **StructlogLogger** in dev/production (logs to console/Loki)
- **NullLogger** in tests (silent)

No need to check environment in your code - the dependency injection handles it.

### 3. Use Structured Logging

Always pass context as keyword arguments, never in the message string.

```python
# Good - structured data
self._logger.info("Login attempt", email=email, user_id=user_id)
self._logger.warning("Account blocked", user_id=user_id, blocked_until=timestamp)

# Bad - unstructured string formatting
self._logger.info(f"Login attempt for {email}")  # Can't query by email in Loki!
self._logger.warning(f"User {user_id} blocked until {timestamp}")  # Can't filter!
```

**Benefits of structured logging:**
- Queryable in Grafana: `{app="homecomp-api"} | json | email="user@example.com"`
- Type-safe: Loki indexes fields automatically
- Machine-readable: Easy to aggregate, alert, visualize

## Log Levels

Use appropriate log levels according to severity:

### debug
**When**: Detailed diagnostic information useful during development
**Examples**:
- Method entry/exit
- Internal state transitions
- Query parameters

```python
self._logger.debug("Handling login command", email=command.email)
self._logger.debug("No existing session, creating new session", user_id=user_id)
self._logger.debug("Applying login delay", delay_seconds=delay)
```

### info
**When**: Normal application flow, significant events
**Examples**:
- Successful operations
- User actions
- State changes

```python
self._logger.info("Login attempt", email=email)
self._logger.info("Login successful", email=email, user_id=user_id)
self._logger.info("Password verified successfully", user_id=user_id)
```

### warning
**When**: Recoverable errors, security events, degraded functionality
**Examples**:
- Failed authentication (expected behavior)
- Rate limiting triggered
- Retryable failures

```python
self._logger.warning("Login failed - invalid credentials", email=email)
self._logger.warning("Account blocked", user_id=user_id, blocked_until=timestamp)
self._logger.warning("Max login attempts reached", user_id=user_id)
```

### error
**When**: Unexpected errors that need investigation
**Examples**:
- Database errors
- Invalid data from trusted sources
- Unhandled exceptions

```python
self._logger.error("Token generation failed", email=email)
self._logger.error("Invalid user data retrieved from database", email=email)
self._logger.error("Unexpected error during login", email=email, error=str(e))
```

### critical
**When**: System failures requiring immediate attention
**Examples**:
- Database connection lost
- Critical service unavailable
- Data corruption detected

```python
self._logger.critical("Database connection pool exhausted")
self._logger.critical("Unable to connect to authentication service", error=str(e))
```

## Logging Strategy by Layer

### CRITICAL RULE: Avoid Redundant Success Logs

**DO NOT log successful operations at multiple layers.** This creates log bloat and makes debugging harder.

**Pattern**: Log success **ONLY at the controller layer** for audit trail purposes.

```python
# ✅ GOOD - Success logged only at controller
@router.post("/cards")
async def create_credit_card(
    request: CreateCreditCardRequest,
    handler: CreateCreditCardHandlerContract = Depends(...),
    logger: LoggerContract = Depends(get_logger),
):
    logger.info("Create credit card request", user_id=user_id, name=request.name)
    result = await handler.handle(command)

    # Log success at controller level (audit trail)
    logger.info("Credit card created successfully", user_id=user_id, credit_card_id=result.id)
    return response

# ✅ GOOD - Handler logs only errors/warnings, NOT success
class CreateCreditCardHandler:
    async def handle(self, command):
        try:
            card = await self._service.create(...)
            return CreateCreditCardResult(credit_card_id=card.id)  # No success log
        except CreditCardNameAlreadyExistError:
            self._logger.debug("Card name already exists", user_id=command.user_id)
            return CreateCreditCardResult(error_code=...)

# ✅ GOOD - Service logs only business events, NOT success
class CreateCreditCardService:
    async def create(self, user_id, name, ...):
        self._logger.debug("Creating credit card", user_id=user_id.value, name=name.value)
        # ... business logic ...
        return await self._repository.save(card)  # No success log
```

```python
# ❌ BAD - Success logged at all layers (redundant!)
@router.post("/cards")
async def create_credit_card(...):
    logger.info("Create credit card request", ...)
    result = await handler.handle(command)
    logger.info("Credit card created successfully", ...)  # ✅ Keep this one
    return response

class CreateCreditCardHandler:
    async def handle(self, command):
        card = await self._service.create(...)
        self._logger.info("Handler succeeded", ...)  # ❌ Remove - redundant!
        return CreateCreditCardResult(...)

class CreateCreditCardService:
    async def create(...):
        result = await self._repository.save(card)
        self._logger.info("Card created", ...)  # ❌ Remove - redundant!
        return result
```

**Why this matters**:
- **Audit trail**: Controller logs capture what happened (one log = one operation)
- **Less noise**: Easier to find errors when not buried in success logs
- **Better performance**: Fewer logs = lower overhead
- **Cleaner queries**: `{severity="error"}` shows real problems, not buried in success logs

**What to log at each layer**:
- **Controllers**: Success (info), errors/warnings for HTTP outcomes
- **Handlers**: Only errors, business rule violations, cross-context calls (debug)
- **Services**: Only business events (warnings), errors, debug flow

### Controller Layer (Interface/REST)

**Purpose**: Log HTTP-level events and user-facing outcomes

**What to log**:
- Incoming requests (info)
- Success responses (info)
- Client errors 4xx (warning)
- Server errors 5xx (error)

**What NOT to log**:
- Passwords or sensitive data
- Internal implementation details (use handler/service for that)

```python
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger

@router.post("/login")
async def login(
    request: LoginRequest,
    handler: Annotated[LoginHandlerContract, Depends(get_login_handler)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
):
    logger.info("Login attempt", email=str(request.email))

    result = await handler.handle(LoginCommand(...))

    if result.status == LoginHandlerResultStatus.SUCCESS:
        logger.info("Login successful", email=str(request.email), user_id=result.user_id)
        return LoginResponse(message="Login successful")

    if result.status == LoginHandlerResultStatus.INVALID_CREDENTIALS:
        logger.warning("Login failed - invalid credentials", email=str(request.email))
        raise HTTPException(status_code=401, detail=result.error_msg)

    if result.status == LoginHandlerResultStatus.ACCOUNT_BLOCKED:
        logger.warning(
            "Login failed - account blocked",
            email=str(request.email),
            retry_after=result.retry_after.isoformat() if result.retry_after else None,
        )
        raise HTTPException(status_code=429, detail=result.error_msg)

    logger.error("Login failed - unexpected error", email=str(request.email), status=result.status.value)
    raise HTTPException(status_code=500, detail=result.error_msg)
```

### Handler Layer (Application)

**Purpose**: Log orchestration logic and business flow

**What to log**:
- Handler execution start (debug)
- Cross-context calls (debug)
- Business rule violations (info/warning)
- Exception handling (error)

```python
from app.shared.domain.contracts import LoggerContract

class LoginHandler(LoginHandlerContract):
    def __init__(
        self,
        user_handler: FindUserHandlerContract,
        login_service: LoginServiceContract,
        logger: LoggerContract,
    ):
        self._user_handler = user_handler
        self._login_service = login_service
        self._logger = logger

    async def handle(self, command: LoginCommand) -> LoginHandlerResultDTO:
        self._logger.debug("Handling login command", email=command.email)

        user = await self._user_handler.handle(FindUserQuery(email=command.email))
        if user is None or user.error_code is not None:
            self._logger.debug("User not found", email=command.email)
            return LoginHandlerResultDTO(
                status=LoginHandlerResultStatus.INVALID_CREDENTIALS,
                error_msg="Invalid username or password",
            )

        if user.user_id is None or user.email is None or user.password is None:
            self._logger.error("Invalid user data retrieved from database", email=command.email)
            return LoginHandlerResultDTO(
                status=LoginHandlerResultStatus.UNEXPECTED_ERROR,
                error_msg="Invalid user data",
            )

        try:
            user_token = await self._login_service.handle(...)
            self._logger.debug("Login service succeeded", email=command.email, user_id=user.user_id)
            return LoginHandlerResultDTO(status=LoginHandlerResultStatus.SUCCESS, ...)

        except AccountBlockedException as abe:
            self._logger.info(
                "Account blocked",
                email=command.email,
                blocked_until=abe.blocked_until.isoformat() if abe.blocked_until else None,
            )
            return LoginHandlerResultDTO(status=LoginHandlerResultStatus.ACCOUNT_BLOCKED, ...)

        except InvalidCredentialsException:
            self._logger.debug("Invalid credentials provided", email=command.email)
            return LoginHandlerResultDTO(status=LoginHandlerResultStatus.INVALID_CREDENTIALS, ...)

        except Exception as e:
            self._logger.error("Unexpected error during login", email=command.email, error=str(e))
            return LoginHandlerResultDTO(status=LoginHandlerResultStatus.UNEXPECTED_ERROR, ...)
```

### Service Layer (Domain)

**Purpose**: Log domain logic execution and business rule enforcement

**What to log**:
- Service method entry (debug)
- Business rule evaluations (info)
- Domain exceptions (warning/error)
- State changes (info)

```python
from app.shared.domain.contracts import LoggerContract

class LoginService(LoginServiceContract):
    def __init__(self, session_repo: SessionRepositoryContract, logger: LoggerContract):
        self._session_repo = session_repo
        self._logger = logger

    async def handle(self, user_password: AuthPassword, db_user: AuthUserDTO) -> SessionToken:
        self._logger.debug("Login service started", user_id=db_user.user_id.value, email=db_user.email.value)

        session = await self._session_repo.getSession(user_id=db_user.user_id)

        if session is None:
            self._logger.debug("No existing session, creating new session", user_id=db_user.user_id.value)
            session = await self._session_repo.createSession(...)

        if session.blocked_until is not None and not session.blocked_until.isOver():
            self._logger.warning(
                "Account is blocked",
                user_id=db_user.user_id.value,
                blocked_until=session.blocked_until.value.isoformat(),
            )
            raise AccountBlockedException(session.blocked_until.value)

        if not db_user.password.verify(user_password.value):
            new_attempts = FailedLoginAttempts(session.failed_attempts.value + 1)

            self._logger.info(
                "Password verification failed",
                user_id=db_user.user_id.value,
                failed_attempts=new_attempts.value,
            )

            if new_attempts.hasReachMaxAttempts():
                blocked_until = BlockedTime.setBlocked()
                self._logger.warning(
                    "Max login attempts reached, blocking account",
                    user_id=db_user.user_id.value,
                    blocked_until=blocked_until.value.isoformat(),
                )

            await self._session_repo.updateSession(...)

            delay = new_attempts.getAttemptDelay()
            self._logger.debug("Applying login delay", delay_seconds=delay)
            await asyncio.sleep(delay)

            raise InvalidCredentialsException()

        new_token = SessionToken.generate()
        self._logger.info(
            "Password verified successfully, creating session token",
            user_id=db_user.user_id.value,
        )

        await self._session_repo.updateSession(...)
        return new_token
```

## Dependency Injection Setup

### Step 1: Add Logger to Constructor

```python
from app.shared.domain.contracts import LoggerContract

class MyService:
    def __init__(
        self,
        some_repo: SomeRepositoryContract,
        logger: LoggerContract,  # Add logger parameter
    ):
        self._some_repo = some_repo
        self._logger = logger
```

### Step 2: Update Dependency Factory

```python
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger

def get_my_service(
    some_repo: Annotated[SomeRepositoryContract, Depends(get_some_repo)],
    logger: Annotated[LoggerContract, Depends(get_logger)],  # Add logger dependency
) -> MyServiceContract:
    return MyService(some_repo, logger)
```

### Step 3: Controllers Get Logger Directly

Controllers inject logger as a parameter (not passed through handlers):

```python
@router.post("/endpoint")
async def my_endpoint(
    request: MyRequest,
    handler: Annotated[MyHandlerContract, Depends(get_my_handler)],
    logger: Annotated[LoggerContract, Depends(get_logger)],  # Inject logger
):
    logger.info("Request received", some_field=request.some_field)
    result = await handler.handle(...)
    logger.info("Request completed", result_status=result.status)
    return result
```

## Security Considerations

### Never Log Sensitive Data

**Never log**:
- Passwords (plain text or hashed)
- Session tokens
- API keys
- Credit card numbers
- Personal identifiable information (unless absolutely necessary)

```python
# Bad - logs password
self._logger.info("User login", email=email, password=password)  # NEVER!

# Bad - logs session token
self._logger.info("Session created", token=token.value)  # NEVER!

# Good - logs only non-sensitive data
self._logger.info("Login successful", email=email, user_id=user_id)
```

### Log Security Events

Always log security-relevant events:
- Authentication attempts (success and failure)
- Authorization failures
- Rate limiting triggers
- Account lockouts
- Suspicious activity

```python
self._logger.warning("Login failed - invalid credentials", email=email)
self._logger.warning("Account blocked due to max attempts", user_id=user_id)
self._logger.warning("Unauthorized access attempt", user_id=user_id, resource=resource)
```

## Performance Considerations

### Use Appropriate Log Levels

In production, set log level to `INFO` to avoid debug overhead:
- Debug logs are skipped entirely (no string formatting)
- Info/warning/error logs are processed

### Avoid Expensive Operations in Log Calls

```python
# Bad - expensive operation even if debug is disabled
self._logger.debug("User data", user_data=json.dumps(expensive_serialize(user)))

# Good - expensive operation only if debug enabled
if self._logger._logger.isEnabledFor(logging.DEBUG):
    self._logger.debug("User data", user_data=json.dumps(expensive_serialize(user)))

# Best - keep it simple
self._logger.debug("User loaded", user_id=user.id)
```

## Querying Logs in Grafana

### Basic Queries

```logql
# All application logs
{app="homecomp-api"}

# Filter by severity
{app="homecomp-api", severity="warning"}
{app="homecomp-api", severity="error"}

# Search for specific events
{app="homecomp-api"} |= "Login attempt"
{app="homecomp-api"} |= "Account blocked"
```

### Structured Queries

```logql
# Parse JSON and filter by field
{app="homecomp-api"} | json | email="user@example.com"
{app="homecomp-api"} | json | user_id="123"
{app="homecomp-api"} | json | level="error"

# Count events
count_over_time({app="homecomp-api"} |= "Login attempt" [5m])

# Aggregate by field
sum by (email) (count_over_time({app="homecomp-api"} |= "Login failed" [1h]))
```

### Advanced Queries

```logql
# Failed logins in last hour
{app="homecomp-api", severity="warning"} |= "Login failed" [1h]

# Errors by logger
sum by (logger) (count_over_time({app="homecomp-api", severity="error"} [1h]))

# Login attempts per email
topk(10, sum by (email) (count_over_time({app="homecomp-api"} |= "Login attempt" [24h])))
```

## Testing

### Unit Tests

Logger is automatically replaced with `NullLogger` when `APP_ENV=test`:

```python
# In tests, logger does nothing - no output, no setup needed
def test_login_handler():
    logger = get_logger()  # Returns NullLogger in test environment
    handler = LoginHandler(user_handler, login_service, logger)
    # Logger calls are no-ops, tests run silently
```

### Integration Tests

If you need to verify logging behavior:

```python
from app.shared.infrastructure.logging import StructlogLogger

def test_login_logs_attempt():
    # Create real logger for verification
    logger = StructlogLogger()
    handler = LoginHandler(user_handler, login_service, logger)

    # Use caplog fixture to capture logs
    result = handler.handle(LoginCommand(email="test@example.com", password="wrong"))

    # Verify log was called (implementation depends on test framework)
    # Usually not necessary - focus on behavior, not logging
```

**Recommendation**: Don't test logging in unit tests. Logging is a cross-cutting concern - verify business logic instead.

## Common Patterns

### Login/Authentication Flow

```python
# Controller
logger.info("Login attempt", email=email)
# Handler
logger.debug("Handling login command", email=email)
# Service
logger.info("Password verification failed", user_id=user_id, failed_attempts=3)
logger.warning("Max login attempts reached, blocking account", user_id=user_id)
```

### CRUD Operations

```python
# Create
logger.info("Creating account", user_id=user_id, account_name=name)
logger.info("Account created", account_id=account_id)

# Read
logger.debug("Fetching account", account_id=account_id)

# Update
logger.info("Updating account", account_id=account_id, fields=["balance"])
logger.info("Account updated", account_id=account_id)

# Delete
logger.warning("Deleting account", account_id=account_id, user_id=user_id)
logger.info("Account deleted", account_id=account_id)
```

### Error Handling

```python
try:
    result = await some_operation()
    logger.info("Operation succeeded", operation="some_operation", result_id=result.id)
except SpecificException as e:
    logger.warning("Expected failure", operation="some_operation", error=str(e))
    raise
except Exception as e:
    logger.error("Unexpected error", operation="some_operation", error=str(e))
    raise
```

## Summary Checklist

When adding logging to a new feature:

- [ ] Inject `LoggerContract` via dependency injection
- [ ] Add logger to dependency factory functions
- [ ] Log at controller layer (user-facing events)
- [ ] Log at handler layer (orchestration flow)
- [ ] Log at service layer (domain logic)
- [ ] Use appropriate log levels (debug/info/warning/error/critical)
- [ ] Pass context as keyword arguments (structured logging)
- [ ] Never log sensitive data (passwords, tokens, etc.)
- [ ] Log security events (auth failures, rate limits, etc.)
- [ ] Test in dev environment - verify logs appear in console and Grafana
