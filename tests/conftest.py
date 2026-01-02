"""Global test configuration and fixture imports.

This file imports fixtures from the organized fixtures/ directory structure.
Add global fixtures here if they're truly shared across all contexts.
"""

# Import shared fixtures
# Import auth context fixtures
from tests.fixtures.auth import (
    MockLoginService,
    MockSessionRepository,
    mock_login_service,
    mock_session_repository,
)
from tests.fixtures.shared import mock_logger

# Import user context fixtures
from tests.fixtures.user import MockFindUserHandler, mock_find_user_handler

# Import user_account context fixtures
from tests.fixtures.user_account import (
    sample_account_dto,
    sample_account_id,
    sample_account_model,
    sample_account_name,
    sample_balance,
    sample_currency,
    sample_deleted_account_dto,
    sample_deleted_account_model,
    sample_new_account_dto,
    sample_user_id,
)

# Make fixtures available to pytest
__all__ = [
    # Shared fixtures
    "mock_logger",
    # Auth fixtures
    "MockSessionRepository",
    "mock_session_repository",
    "MockLoginService",
    "mock_login_service",
    # User fixtures
    "MockFindUserHandler",
    "mock_find_user_handler",
    # User account fixtures
    "sample_user_id",
    "sample_account_id",
    "sample_account_name",
    "sample_currency",
    "sample_balance",
    "sample_account_dto",
    "sample_new_account_dto",
    "sample_deleted_account_dto",
    "sample_account_model",
    "sample_deleted_account_model",
]
