from fastapi import APIRouter

from app.context.user_account.interface.rest.controllers import create_account_router

user_account_routes = APIRouter(prefix="/api/user-accounts", tags=["user-accounts"])

# Include all controller routers
user_account_routes.include_router(create_account_router)
