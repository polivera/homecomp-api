from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_db
from app.context.auth.interface.rest.controllers import loginAction, user_router
from app.context.auth.interface.rest.schemas import LoginRequest

auth_routes = APIRouter(prefix="/api/auth", tags=["auth"])

# Include user router (with dependency injection chain)
auth_routes.include_router(user_router)


@auth_routes.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await loginAction(request)
