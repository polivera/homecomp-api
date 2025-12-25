---
paths: tests/**/*.py
---

# Testing Guidelines

## Test Organization

Structure tests to mirror the DDD architecture:

```
tests/
├── unit/
│   ├── context/
│   │   ├── auth/
│   │   │   ├── domain/          # Value objects, domain services
│   │   │   ├── application/     # Handlers with mocked dependencies
│   │   │   └── infrastructure/  # Repositories with test DB
│   │   └── user/
│   └── shared/
└── integration/
    └── test_*.py                # API endpoint tests
```

## Framework and Tools

- Use `pytest` with `pytest-asyncio` for async test support
- Use `pytest-cov` for coverage reporting
- Use `httpx.AsyncClient` for integration testing FastAPI endpoints
- Use `pytest.mark.asyncio` decorator for all async tests

## Unit Test Patterns

### Testing Value Objects

Always test validation logic extensively:

```python
def test_email_validation_rejects_invalid_format():
    with pytest.raises(ValueError, match="Invalid email"):
        Email("not-an-email")

def test_email_validation_accepts_valid_format():
    email = Email("user@example.com")
    assert email.value == "user@example.com"
```

### Testing Domain Services

Mock repository contracts, never implementations:

```python
@pytest.mark.asyncio
async def test_login_service_with_valid_credentials():
    # Arrange
    mock_repo = Mock(spec=UserRepositoryContract)
    mock_repo.find_user.return_value = UserDTO(...)

    service = LoginService(mock_repo)

    # Act
    result = await service.login(email, password)

    # Assert
    assert result.is_success
    mock_repo.find_user.assert_called_once()
```

### Testing Handlers

Inject mocked service contracts:

```python
@pytest.mark.asyncio
async def test_login_handler_returns_token_on_success():
    # Arrange
    mock_service = Mock(spec=LoginServiceContract)
    mock_service.login.return_value = LoginResultDTO(...)

    handler = LoginHandler(mock_service)
    command = LoginCommand(email=Email(...), password=Password(...))

    # Act
    result = await handler.handle(command)

    # Assert
    assert result.token is not None
```

## Integration Test Patterns

### Testing Endpoints

Use FastAPI's test client with async support:

```python
@pytest.mark.asyncio
async def test_login_endpoint_returns_200_with_valid_credentials(client: AsyncClient):
    response = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "ValidPass123"}
    )

    assert response.status_code == 200
    assert "token" in response.json()
```

### Testing Repository Implementations

Use a test database (not mocks):

```python
@pytest.mark.asyncio
async def test_user_repository_finds_user_by_email(test_db: AsyncSession):
    # Arrange
    repo = UserRepository(test_db)
    # Insert test data...

    # Act
    user = await repo.find_user(email=Email("test@example.com"))

    # Assert
    assert user is not None
    assert user.email.value == "test@example.com"
```

## Test Fixtures

Create reusable fixtures in `conftest.py`:

```python
# tests/conftest.py
@pytest.fixture
async def test_db():
    """Provide clean test database session"""
    # Setup test database
    # Yield session
    # Teardown/rollback

@pytest.fixture
async def client():
    """Provide FastAPI test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
```

## Coverage Requirements

- Aim for 80%+ coverage on domain and application layers
- 100% coverage on value object validation logic
- Infrastructure can have lower coverage (e.g., 60%)
- Don't test framework code (FastAPI internals)

## Test Naming

Use descriptive names following the pattern:
- `test_{unit}__{scenario}__{expected_behavior}`
- Example: `test_login_service__invalid_password__raises_authentication_error`

## What NOT to Test

- SQLAlchemy's ORM functionality
- FastAPI's request parsing
- Third-party library internals
- Trivial property getters on dataclasses

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/context/auth/domain/test_login_service.py

# Run tests matching pattern
pytest -k "login"
```
