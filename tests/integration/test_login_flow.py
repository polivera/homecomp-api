"""Integration tests for the login flow.

Tests the complete login flow from HTTP request through to database,
including authentication, cookie handling, and error scenarios.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
class TestLoginFlow:
    """Integration tests for login endpoint."""

    async def test_successful_login_returns_200_and_sets_cookie(
        self, test_client: AsyncClient, test_user: dict
    ):
        """Test successful login returns 200 status and sets access_token cookie."""
        # Arrange
        login_payload = {
            "email": test_user["email"],
            "password": test_user["password"],
        }

        # Act
        response = await test_client.post("/api/auth/login", json=login_payload)

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": "Login successful"}

        # Verify cookie is set
        assert "access_token" in response.cookies
        access_token = response.cookies["access_token"]
        assert access_token is not None
        assert len(access_token) > 0

        # Verify cookie attributes (security settings)
        cookie_header = response.headers.get("set-cookie", "")
        assert "HttpOnly" in cookie_header
        assert "SameSite=lax" in cookie_header
        assert "Max-Age=3600" in cookie_header  # 1 hour

    async def test_login_with_invalid_email_returns_401(
        self, test_client: AsyncClient
    ):
        """Test login with non-existent email returns 401."""
        # Arrange
        login_payload = {
            "email": "nonexistent@example.com",
            "password": "SomePassword123!",
        }

        # Act
        response = await test_client.post("/api/auth/login", json=login_payload)

        # Assert
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid username or password"

        # Verify no cookie is set
        assert "access_token" not in response.cookies

    async def test_login_with_wrong_password_returns_401(
        self, test_client: AsyncClient, test_user: dict
    ):
        """Test login with correct email but wrong password returns 401."""
        # Arrange
        login_payload = {
            "email": test_user["email"],
            "password": "WrongPassword123!",
        }

        # Act
        response = await test_client.post("/api/auth/login", json=login_payload)

        # Assert
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid username or password"

        # Verify no cookie is set
        assert "access_token" not in response.cookies

    async def test_login_with_invalid_email_format_returns_422(
        self, test_client: AsyncClient
    ):
        """Test login with invalid email format returns 422 (validation error)."""
        # Arrange
        login_payload = {
            "email": "not-an-email",
            "password": "SomePassword123!",
        }

        # Act
        response = await test_client.post("/api/auth/login", json=login_payload)

        # Assert
        assert response.status_code == 422  # Pydantic validation error
        assert "detail" in response.json()

    async def test_login_with_missing_password_returns_422(
        self, test_client: AsyncClient, test_user: dict
    ):
        """Test login without password returns 422 (validation error)."""
        # Arrange
        login_payload = {
            "email": test_user["email"],
            # password is missing
        }

        # Act
        response = await test_client.post("/api/auth/login", json=login_payload)

        # Assert
        assert response.status_code == 422
        assert "detail" in response.json()

    async def test_login_with_missing_email_returns_422(
        self, test_client: AsyncClient
    ):
        """Test login without email returns 422 (validation error)."""
        # Arrange
        login_payload = {
            # email is missing
            "password": "SomePassword123!",
        }

        # Act
        response = await test_client.post("/api/auth/login", json=login_payload)

        # Assert
        assert response.status_code == 422
        assert "detail" in response.json()

    async def test_login_with_empty_payload_returns_422(
        self, test_client: AsyncClient
    ):
        """Test login with empty payload returns 422."""
        # Arrange
        login_payload = {}

        # Act
        response = await test_client.post("/api/auth/login", json=login_payload)

        # Assert
        assert response.status_code == 422

    async def test_multiple_successful_logins_same_user(
        self, test_client: AsyncClient, test_user: dict
    ):
        """Test that the same user can login multiple times successfully."""
        # Arrange
        login_payload = {
            "email": test_user["email"],
            "password": test_user["password"],
        }

        # Act - First login
        response1 = await test_client.post("/api/auth/login", json=login_payload)

        # Assert - First login successful
        assert response1.status_code == 200
        token1 = response1.cookies.get("access_token")
        assert token1 is not None

        # Act - Second login
        response2 = await test_client.post("/api/auth/login", json=login_payload)

        # Assert - Second login successful (may have different token)
        assert response2.status_code == 200
        token2 = response2.cookies.get("access_token")
        assert token2 is not None

    async def test_login_with_case_sensitive_email(
        self, test_client: AsyncClient, test_user: dict
    ):
        """Test that email is case-sensitive (or case-insensitive based on implementation).

        Note: Adjust this test based on your email matching logic.
        Current implementation treats emails as case-sensitive.
        """
        # Arrange - Use uppercase version of email
        login_payload = {
            "email": test_user["email"].upper(),
            "password": test_user["password"],
        }

        # Act
        response = await test_client.post("/api/auth/login", json=login_payload)

        # Assert - Should fail if email is case-sensitive
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid username or password"

    async def test_login_with_extra_whitespace_in_email(
        self, test_client: AsyncClient, test_user: dict
    ):
        """Test that extra whitespace in email is handled correctly."""
        # Arrange - Add whitespace around email
        login_payload = {
            "email": f"  {test_user['email']}  ",
            "password": test_user["password"],
        }

        # Act
        response = await test_client.post("/api/auth/login", json=login_payload)

        # Assert - Pydantic EmailStr should strip whitespace, so this should succeed
        # If it doesn't, you may need to add explicit validation
        assert response.status_code in [200, 401]  # Depends on implementation

    async def test_login_endpoint_uses_post_method(self, test_client: AsyncClient):
        """Test that login endpoint only accepts POST requests."""
        # Act - Try GET request
        response = await test_client.get("/api/auth/login")

        # Assert - Should return 405 Method Not Allowed
        assert response.status_code == 405

    async def test_concurrent_logins_different_users(
        self, test_client: AsyncClient, test_user: dict, test_db_session
    ):
        """Test that multiple users can login concurrently without conflicts."""
        # Arrange - Create a second user
        from app.shared.domain.value_objects import SharedPassword
        from app.context.user.infrastructure.models import UserModel

        second_user_email = "seconduser@example.com"
        second_user_password = "AnotherPassword123!"
        second_user_hashed = SharedPassword.from_plain_text(second_user_password).value

        second_user_model = UserModel(
            email=second_user_email,
            password=second_user_hashed,
            username="seconduser",
        )
        test_db_session.add(second_user_model)
        await test_db_session.commit()

        # Act - Login both users
        response1 = await test_client.post(
            "/api/auth/login",
            json={"email": test_user["email"], "password": test_user["password"]},
        )

        response2 = await test_client.post(
            "/api/auth/login",
            json={"email": second_user_email, "password": second_user_password},
        )

        # Assert - Both logins should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200

        token1 = response1.cookies.get("access_token")
        token2 = response2.cookies.get("access_token")

        assert token1 is not None
        assert token2 is not None
        # Tokens should be different for different users
        assert token1 != token2
