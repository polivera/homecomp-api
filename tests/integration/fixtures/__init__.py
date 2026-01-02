"""Integration test fixtures organized by category."""

# Import database fixtures
# Import client fixtures
from tests.integration.fixtures.client import test_client
from tests.integration.fixtures.database import (
    test_db_session,
    test_engine,
)

# Import user fixtures
from tests.integration.fixtures.users import (
    blocked_user,
    test_user,
)

# Make fixtures available to pytest
__all__ = [
    # Database fixtures
    "test_engine",
    "test_db_session",
    # Client fixtures
    "test_client",
    # User fixtures
    "test_user",
    "blocked_user",
]
