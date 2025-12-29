"""Unit tests for SessionToken value object"""

import pytest

from app.context.auth.domain.value_objects import SessionToken


@pytest.mark.unit
class TestSessionToken:
    """Tests for SessionToken value object"""

    def test_generate_creates_valid_token(self):
        """Test that generate creates a valid token string"""
        token = SessionToken.generate()

        assert token.value is not None
        assert isinstance(token.value, str)
        assert len(token.value) > 0

    def test_generate_creates_unique_tokens(self):
        """Test that generate creates unique tokens each time"""
        token1 = SessionToken.generate()
        token2 = SessionToken.generate()
        token3 = SessionToken.generate()

        # All tokens should be unique
        assert token1.value != token2.value
        assert token2.value != token3.value
        assert token1.value != token3.value

    def test_generate_creates_url_safe_tokens(self):
        """Test that generated tokens are URL-safe"""
        token = SessionToken.generate()

        # URL-safe tokens should not contain special characters like +, /, =
        assert "+" not in token.value
        assert "/" not in token.value
        # Note: = padding is removed in urlsafe_b64encode

    def test_from_string_creates_token_from_existing_string(self):
        """Test that from_string creates token from existing string"""
        existing_token = "my-existing-token-123"
        token = SessionToken.from_string(existing_token)

        assert token.value == existing_token

    def test_direct_construction(self):
        """Test that token can be constructed directly with value"""
        token_value = "direct-token-value"
        token = SessionToken(value=token_value)

        assert token.value == token_value

    def test_immutability(self):
        """Test that value object is immutable"""
        token = SessionToken.generate()
        with pytest.raises(Exception):  # FrozenInstanceError
            token.value = "modified-token"

    def test_equality(self):
        """Test that two SessionToken objects with same value are equal"""
        token_value = "same-token-value"
        token1 = SessionToken(value=token_value)
        token2 = SessionToken(value=token_value)

        assert token1 == token2

    def test_inequality(self):
        """Test that two SessionToken objects with different values are not equal"""
        token1 = SessionToken.generate()
        token2 = SessionToken.generate()

        assert token1 != token2

    def test_generated_token_has_sufficient_entropy(self):
        """Test that generated tokens have sufficient length for security"""
        token = SessionToken.generate()

        # tokens generated with secrets.token_urlsafe(32) should be ~43 chars
        # (32 bytes -> 256 bits of entropy)
        assert len(token.value) >= 40  # Reasonable minimum for security
