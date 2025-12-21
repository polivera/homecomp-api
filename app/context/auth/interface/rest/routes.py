from fastapi import APIRouter

from app.context.auth.interface.rest.controllers import login_router

auth_routes = APIRouter(prefix="/api/auth", tags=["auth"])

# Include all controller routers
auth_routes.include_router(login_router)
