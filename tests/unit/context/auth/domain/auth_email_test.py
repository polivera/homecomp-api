"""Unit tests for AuthEmail value object"""

from dataclasses import FrozenInstanceError

import pytest

from app.context.auth.domain.value_objects import AuthEmail


@pytest.mark.unit
class TestAuthEmail:
    """Tests for AuthEmail value object"""

    def test_valid_email_creation(self):
        """Test creating valid email addresses"""
        email = AuthEmail("user@example.com")
        assert email.value == "user@example.com"

    def test_various_valid_email_formats(self):
        """Test that various valid email formats are accepted"""
        valid_emails = [
            "simple@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "test123@subdomain.example.org",
            "test@domain.co",
        ]
        for email_str in valid_emails:
            email = AuthEmail(email_str)
            assert email.value == email_str

    def test_invalid_email_missing_at_symbol_raises_error(self):
        """Test that email without @ raises ValueError"""
        with pytest.raises(ValueError, match="Invalid email"):
            AuthEmail("notanemail.com")

    def test_invalid_email_missing_domain_raises_error(self):
        """Test that email without domain raises ValueError"""
        with pytest.raises(ValueError, match="Invalid email"):
            AuthEmail("user@")

    def test_invalid_email_missing_local_part_raises_error(self):
        """Test that email without local part raises ValueError"""
        with pytest.raises(ValueError, match="Invalid email"):
            AuthEmail("@example.com")

    def test_invalid_email_empty_string_raises_error(self):
        """Test that empty string raises ValueError"""
        with pytest.raises(ValueError, match="Email cannot be empty"):
            AuthEmail("")

    def test_from_trusted_source_skips_validation(self):
        """Test that from_trusted_source bypasses validation"""
        # This should work even with invalid email
        email = AuthEmail.from_trusted_source("not-a-valid-email")
        assert email.value == "not-a-valid-email"

    def test_immutability(self):
        """Test that value object is immutable"""
        email = AuthEmail("test@example.com")
        with pytest.raises(FrozenInstanceError):
            email.value = "changed@example.com"

    def test_equality(self):
        """Test that two AuthEmail objects with same value are equal"""
        email1 = AuthEmail("same@example.com")
        email2 = AuthEmail("same@example.com")
        assert email1 == email2

    def test_inequality(self):
        """Test that two AuthEmail objects with different values are not equal"""
        email1 = AuthEmail("user1@example.com")
        email2 = AuthEmail("user2@example.com")
        assert email1 != email2
