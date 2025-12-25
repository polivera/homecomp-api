"""Integration test configuration and fixture imports.

This file imports fixtures from the organized fixtures/ directory structure.
Add global integration test fixtures here if they're truly shared across all integration tests.
"""

# Import database fixtures
from tests.integration.fixtures.database import (
    test_db_session,
    test_engine,
)

# Import client fixtures
from tests.integration.fixtures.client import test_client

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
