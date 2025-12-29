"""Unit tests for AuthUserID value object"""

import pytest

from app.context.auth.domain.value_objects import AuthUserID


@pytest.mark.unit
class TestAuthUserID:
    """Tests for AuthUserID value object"""

    def test_valid_user_id_creation(self):
        """Test creating valid user IDs"""
        user_id = AuthUserID(42)
        assert user_id.value == 42

    def test_various_valid_user_ids(self):
        """Test that various valid user IDs are accepted"""
        valid_ids = [1, 100, 999, 123456, 9999999]
        for id_value in valid_ids:
            user_id = AuthUserID(id_value)
            assert user_id.value == id_value

    def test_zero_user_id(self):
        """Test that zero is a valid user ID"""
        user_id = AuthUserID(0)
        assert user_id.value == 0

    def test_immutability(self):
        """Test that value object is immutable"""
        user_id = AuthUserID(123)
        with pytest.raises(Exception):  # FrozenInstanceError
            user_id.value = 456

    def test_equality(self):
        """Test that two AuthUserID objects with same value are equal"""
        user_id1 = AuthUserID(42)
        user_id2 = AuthUserID(42)
        assert user_id1 == user_id2

    def test_inequality(self):
        """Test that two AuthUserID objects with different values are not equal"""
        user_id1 = AuthUserID(1)
        user_id2 = AuthUserID(2)
        assert user_id1 != user_id2

    def test_hash_consistency(self):
        """Test that hash is consistent for same value"""
        user_id1 = AuthUserID(100)
        user_id2 = AuthUserID(100)
        assert hash(user_id1) == hash(user_id2)

    def test_can_be_used_in_set(self):
        """Test that AuthUserID can be used in sets"""
        user_ids = {AuthUserID(1), AuthUserID(2), AuthUserID(1)}
        # Should only have 2 unique values
        assert len(user_ids) == 2

    def test_can_be_used_as_dict_key(self):
        """Test that AuthUserID can be used as dictionary key"""
        user_dict = {
            AuthUserID(1): "User One",
            AuthUserID(2): "User Two",
        }
        assert user_dict[AuthUserID(1)] == "User One"
        assert user_dict[AuthUserID(2)] == "User Two"
