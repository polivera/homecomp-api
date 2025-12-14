from fastapi import APIRouter

from app.context.auth.interface.rest.controllers import loginAction
from app.context.auth.interface.rest.schemas import LoginRequest

auth_routes = APIRouter(prefix="/api/auth", tags=["auth"])


@auth_routes.post("/login")
async def login(request: LoginRequest):
    return await loginAction(request)
