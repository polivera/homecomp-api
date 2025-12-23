from os import getenv

from fastapi import APIRouter, Depends, HTTPException, Response

from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.contracts import LoginHandlerContract
from app.context.auth.application.dto import LoginHandlerResultStatus
from app.context.auth.infrastructure.dependencies import get_login_handler
from app.context.auth.interface.rest.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/login", tags=["login"])


@router.post("", response_model=LoginResponse)
async def login(
    response: Response,
    request: LoginRequest,
    handler: LoginHandlerContract = Depends(get_login_handler),
):
    """User login endpoint"""
    login_result = await handler.handle(
        LoginCommand(email=str(request.email), password=request.password)
    )

    if login_result.status == LoginHandlerResultStatus.SUCCESS:
        if login_result.token is None:
            raise HTTPException(status_code=500, detail="Token generation failed")

        # Set JWT token as HTTP-only secure cookie
        response.set_cookie(
            key="access_token",
            value=login_result.token,
            httponly=True,  # Prevents JavaScript access (XSS protection)
            secure=(getenv("APP_ENV", "dev") == "prod"),  # Only send over HTTPS
            samesite="lax",  # CSRF protection
            max_age=3600,  # 1 hour expiration (adjust as needed)
        )

        return LoginResponse(message="Login successful")

    if login_result.status == LoginHandlerResultStatus.INVALID_CREDENTIALS:
        raise HTTPException(status_code=401, detail=login_result.error_msg)

    if login_result.status == LoginHandlerResultStatus.ACCOUNT_BLOCKED:
        headers = {}
        if login_result.retry_after:
            headers["Retry-After"] = login_result.retry_after.isoformat()
        raise HTTPException(
            status_code=429, detail=login_result.error_msg, headers=headers
        )

    # UNEXPECTED_ERROR or any other status
    raise HTTPException(status_code=500, detail=login_result.error_msg)
