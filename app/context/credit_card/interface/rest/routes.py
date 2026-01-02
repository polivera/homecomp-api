from fastapi import APIRouter

from app.context.credit_card.interface.rest.controllers import (
    create_router,
    delete_router,
    find_by_id_router,
    find_by_user_router,
    update_router,
)

credit_card_routes = APIRouter(prefix="/api/credit-cards", tags=["credit-cards"])

# Include all controller routers
credit_card_routes.include_router(create_router)
credit_card_routes.include_router(find_by_id_router)
credit_card_routes.include_router(find_by_user_router)
credit_card_routes.include_router(update_router)
credit_card_routes.include_router(delete_router)
