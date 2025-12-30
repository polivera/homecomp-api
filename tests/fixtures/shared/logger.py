"""Mock logger for testing."""

import pytest

from app.shared.infrastructure.logging.null_logger import NullLogger


@pytest.fixture
def mock_logger():
    """Fixture providing a NullLogger for tests."""
    return NullLogger()
