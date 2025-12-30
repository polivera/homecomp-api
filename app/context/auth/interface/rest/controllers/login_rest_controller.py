from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response

from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.contracts import LoginHandlerContract
from app.context.auth.application.dto import LoginHandlerResultStatus
from app.context.auth.infrastructure.dependencies import get_login_handler
from app.context.auth.interface.rest.schemas import LoginRequest, LoginResponse
from app.shared.domain.contracts import LoggerContract
from app.shared.domain.value_objects import SharedAppEnv
from app.shared.infrastructure.dependencies import get_logger

router = APIRouter(prefix="/login")


@router.post("", response_model=LoginResponse)
async def login(
    response: Response,
    request: LoginRequest,
    handler: Annotated[LoginHandlerContract, Depends(get_login_handler)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
):
    """User login endpoint"""
    logger.info("Login attempt", email=str(request.email))

    login_result = await handler.handle(LoginCommand(email=str(request.email), password=request.password))

    if login_result.status == LoginHandlerResultStatus.SUCCESS:
        if login_result.token is None:
            logger.error("Token generation failed", email=str(request.email))
            raise HTTPException(status_code=500, detail="Token generation failed")

        logger.info("Login successful", email=str(request.email), user_id=login_result.user_id)

        # Set session token as HTTP-only secure cookie
        response.set_cookie(
            key="access_token",
            value=login_result.token,
            httponly=True,
            secure=SharedAppEnv.isProd(),
            samesite="lax",
            max_age=3600,
        )

        return LoginResponse(message="Login successful")

    if login_result.status == LoginHandlerResultStatus.INVALID_CREDENTIALS:
        logger.warning("Login failed - invalid credentials", email=str(request.email))
        raise HTTPException(status_code=401, detail=login_result.error_msg)

    if login_result.status == LoginHandlerResultStatus.ACCOUNT_BLOCKED:
        logger.warning(
            "Login failed - account blocked",
            email=str(request.email),
            retry_after=login_result.retry_after.isoformat() if login_result.retry_after else None,
        )
        headers = {}
        if login_result.retry_after:
            headers["Retry-After"] = login_result.retry_after.isoformat()
        raise HTTPException(status_code=429, detail=login_result.error_msg, headers=headers)

    # UNEXPECTED_ERROR or any other status
    logger.error("Login failed - unexpected error", email=str(request.email), status=login_result.status.value)
    raise HTTPException(status_code=500, detail=login_result.error_msg)
