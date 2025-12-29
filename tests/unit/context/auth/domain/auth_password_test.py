"""Unit tests for AuthPassword value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.auth.domain.value_objects import AuthPassword


@pytest.mark.unit
class TestAuthPassword:
    """Tests for AuthPassword value object"""

    def test_from_plain_text_creates_hashed_password(self):
        """Test that from_plain_text creates a hashed password"""
        plain_password = "SecurePassword123"
        password = AuthPassword.from_plain_text(plain_password)

        # Verify it's hashed (Argon2 hashes start with $argon2)
        assert password.value.startswith("$argon2")
        assert password.value != plain_password

    def test_from_hash_creates_password_from_existing_hash(self):
        """Test that from_hash creates password from existing hash"""
        existing_hash = "$argon2id$v=19$m=65536,t=3,p=4$somehash"
        password = AuthPassword.from_hash(existing_hash)

        assert password.value == existing_hash

    def test_verify_correct_password_returns_true(self):
        """Test that verify returns True for correct password"""
        plain_password = "MyPassword123"
        hashed_password = AuthPassword.from_plain_text(plain_password)

        # Verify with correct password
        assert hashed_password.verify(plain_password) is True

    def test_verify_incorrect_password_returns_false(self):
        """Test that verify returns False for incorrect password"""
        plain_password = "MyPassword123"
        wrong_password = "WrongPassword456"
        hashed_password = AuthPassword.from_plain_text(plain_password)

        # Verify with wrong password
        assert hashed_password.verify(wrong_password) is False

    def test_different_hashes_for_same_password(self):
        """Test that hashing same password twice produces different hashes (due to salt)"""
        plain_password = "SamePassword"
        password1 = AuthPassword.from_plain_text(plain_password)
        password2 = AuthPassword.from_plain_text(plain_password)

        # Hashes should be different due to random salt
        assert password1.value != password2.value

        # But both should verify the same password
        assert password1.verify(plain_password) is True
        assert password2.verify(plain_password) is True

    def test_keep_plain_creates_unhashed_password(self):
        """Test that keep_plain creates password without hashing"""
        plain_password = "PlainPassword123"
        password = AuthPassword.keep_plain(plain_password)

        # Value should be the plain text (used for comparison during login)
        assert password.value == plain_password

    def test_immutability(self):
        """Test that value object is immutable"""
        password = AuthPassword.from_plain_text("test123")
        with pytest.raises(FrozenInstanceError):
            password.value = "changed"

    def test_verify_with_empty_password_returns_false(self):
        """Test that verify returns False for empty password"""
        hashed_password = AuthPassword.from_plain_text("MyPassword123")
        assert hashed_password.verify("") is False

    def test_from_hash_accepts_any_string(self):
        """Test that from_hash accepts any string without validation"""
        # from_hash is used for database values, so it doesn't validate
        raw_value = "raw-unhashed-value"
        password = AuthPassword.from_hash(raw_value)
        assert password.value == raw_value
