from fastapi import APIRouter

from app.context.entry.interface.rest.controllers import (
    create_router,
    delete_router,
    find_router,
    update_router,
)

entry_routes = APIRouter(prefix="/api/entries", tags=["entries"])

entry_routes.include_router(create_router)
entry_routes.include_router(find_router)
entry_routes.include_router(update_router)
entry_routes.include_router(delete_router)
