from fastapi import APIRouter

from app.context.user_account.interface.rest.controllers.create_account_controller import (
    router as create_router,
)
from app.context.user_account.interface.rest.controllers.delete_account_controller import (
    router as delete_router,
)
from app.context.user_account.interface.rest.controllers.find_account_controller import (
    router as find_router,
)
from app.context.user_account.interface.rest.controllers.update_account_controller import (
    router as update_router,
)

user_account_routes = APIRouter(prefix="/api/user-accounts", tags=["user-accounts"])

# Include all controller routers
user_account_routes.include_router(create_router)
user_account_routes.include_router(find_router)
user_account_routes.include_router(update_router)
user_account_routes.include_router(delete_router)
