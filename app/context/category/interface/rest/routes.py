from fastapi import APIRouter

from app.context.category.interface.rest.controllers import (
    create_router,
    delete_router,
    find_by_id_router,
    find_by_user_router,
    update_router,
)

category_routes = APIRouter(prefix="/api/categories", tags=["categories"])

# Include all controller routers
category_routes.include_router(create_router)
category_routes.include_router(find_by_id_router)
category_routes.include_router(find_by_user_router)
category_routes.include_router(update_router)
category_routes.include_router(delete_router)
