from fastapi import APIRouter, Depends

from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.contracts import LoginHandlerContract
from app.context.auth.infrastructure.dependencies import get_login_handler
from app.context.auth.interface.rest.schemas import LoginRequest

router = APIRouter(prefix="/login", tags=["login"])


@router.post("")
async def login(
    request: LoginRequest, handler: LoginHandlerContract = Depends(get_login_handler)
):
    """User login endpoint"""
    return await handler.handle(
        LoginCommand(email=request.email, password=request.password)
    )
