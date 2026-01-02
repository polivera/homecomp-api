"""
Session Authentication Dependency

Provides FastAPI dependency for extracting and validating session tokens
from HTTP-only cookies. Used to protect routes that require authentication.
"""

from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.auth.domain.contracts.session_repository_contract import (
    SessionRepositoryContract,
)
from app.context.auth.domain.value_objects.session_token import SessionToken
from app.context.auth.infrastructure.repositories.session_repository import (
    SessionRepository,
)
from app.shared.infrastructure.database import get_db


def get_session_repository_for_auth(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SessionRepositoryContract:
    """
    Factory function to create session repository for authentication.
    Separate from the main dependencies to avoid circular imports.
    """
    return SessionRepository(db)


async def get_current_user_id(
    session_repo: Annotated[SessionRepositoryContract, Depends(get_session_repository_for_auth)],
    access_token: Annotated[str | None, Cookie()] = None,
) -> int:
    """
    Extract and validate session token from HTTP-only cookie.

    Args:
        access_token: Session token from cookie (automatically extracted by FastAPI)
        session_repo: Session repository for database lookups

    Returns:
        int: The authenticated user's ID

    Raises:
        HTTPException 401: If token is missing, invalid, or session not found
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Wrap token string in SessionToken value object
        token = SessionToken(access_token)

        # Query session by token
        session = await session_repo.getSession(token=token)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Return the user_id as an integer
        return session.user_id.value

    except ValueError as e:
        # SessionToken validation failed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token format: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from ValueError
    except Exception:
        # Unexpected error during session lookup
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service unavailable",
        ) from Exception


async def get_current_user_id_optional(
    session_repo: Annotated[SessionRepositoryContract, Depends(get_session_repository_for_auth)],
    access_token: Annotated[str | None, Cookie()] = None,
) -> int | None:
    """
    Extract and validate session token from HTTP-only cookie (optional version).

    This dependency returns None if no token is present, allowing routes
    to have optional authentication (e.g., public content with personalization).

    Args:
        access_token: Session token from cookie (automatically extracted by FastAPI)
        session_repo: Session repository for database lookups

    Returns:
        Optional[int]: The authenticated user's ID, or None if not authenticated

    Raises:
        HTTPException 401: If token is present but invalid
    """
    if not access_token:
        return None

    try:
        token = SessionToken(access_token)
        session = await session_repo.getSession(token=token)

        if not session:
            # Token provided but invalid - this is suspicious, so we raise
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return session.user_id.value

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token format: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from ValueError
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service unavailable",
        ) from Exception
