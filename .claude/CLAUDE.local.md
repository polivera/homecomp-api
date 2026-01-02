# Personal Development Preferences

This file is for YOUR personal preferences when working on this project.
It's automatically gitignored, so your teammates won't see these.

## My Preferred Patterns

### Error Messages

I prefer verbose error messages during development:

```python
# Instead of:
raise ValueError("Invalid email")

# I prefer:
raise ValueError(
    f"Invalid email format: '{self.value}'. "
    f"Expected format: user@domain.com"
)
```

### Logging

Add debug logging to all service methods:

```python
import logging

logger = logging.getLogger(__name__)

async def login(self, email: Email, password: Password) -> LoginResult:
    logger.debug(f"Attempting login for email: {email.value}")
    # ... implementation
    logger.debug(f"Login successful for email: {email.value}")
```

### Test Data

When creating test fixtures, I prefer these test users:

```python
TEST_USER_EMAIL = "pablo.test@homecomp.dev"
TEST_USER_PASSWORD = "TestPass123!"
```

## My Development Workflow

### Before Starting Work

1. Pull latest changes from `dev` branch
2. Run `just migrate` to ensure DB is up to date
3. Check `docker-compose ps` to verify PostgreSQL is running

### Before Committing

1. Run tests (when test suite exists)
2. Run linter/formatter
3. Review the diff

### Commit Message Style

I prefer conventional commits format:

```
feat(auth): add login throttling service
fix(user): correct email validation regex
refactor(shared): extract password hashing to value object
test(auth): add login service unit tests
```

## Code Review Preferences

When reviewing my code:

- Flag any missing type hints
- Check for proper use of value objects (no raw strings/ints)
- Verify async/await usage
- Ensure repositories return DTOs, not models
- Look for potential N+1 query issues

## Quick Commands I Use

```bash
# Start everything
docker-compose up -d && just run

# Reset database (DESTRUCTIVE!)
docker-compose down -v && docker-compose up -d && just migrate

# Check recent migrations
uv run alembic history | head -n 5

# Database shell
just pgcli
```

## Import Aliases I Like

```python
# Shared value objects
from app.shared.domain.value_objects.shared_email import Email as SharedEmail
from app.shared.domain.value_objects.shared_password import Password as SharedPassword

# Context-specific (when importing across contexts)
from app.context.user.domain.value_objects.user_id import UserID
from app.context.user.domain.dto.user_dto import UserDTO
```

## Notes to Self

- Remember to update CLAUDE.md if architectural patterns change
- Keep `/docs/login-throttle-implementation.md` updated
- Consider adding OpenAPI tags to routes for better docs organization
- Eventually add health check endpoint
- Set up CI/CD when ready

## Personal Testing Preferences

- Always test the happy path first
- Then test validation failures
- Then test edge cases
- Mock at the contract level, never the implementation

## Documentation Standards

When adding new features:

1. Update CLAUDE.md if it affects architecture
2. Add inline comments only for non-obvious business logic
3. Update API docs if adding/changing endpoints
4. Consider adding examples to `/docs/` for complex features
