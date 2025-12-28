"""Unit tests for UserAccountUserID value object"""

import pytest

from app.context.user_account.domain.value_objects import UserAccountUserID


@pytest.mark.unit
class TestUserAccountUserID:
    """Tests for UserAccountUserID value object"""

    def test_valid_user_id_creation(self):
        """Test creating valid user IDs"""
        user_id = UserAccountUserID(1)
        assert user_id.value == 1

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        user_id = UserAccountUserID.from_trusted_source(-999)
        assert user_id.value == -999

    def test_immutability(self):
        """Test that value object is immutable"""
        user_id = UserAccountUserID(1)
        with pytest.raises(Exception):  # FrozenInstanceError
            user_id.value = 2
