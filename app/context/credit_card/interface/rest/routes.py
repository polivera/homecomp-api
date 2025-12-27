from fastapi import APIRouter

from app.context.credit_card.interface.rest.controllers.create_credit_card_controller import (
    router as create_router,
)
from app.context.credit_card.interface.rest.controllers.delete_credit_card_controller import (
    router as delete_router,
)
from app.context.credit_card.interface.rest.controllers.find_credit_card_controller import (
    router as find_router,
)
from app.context.credit_card.interface.rest.controllers.update_credit_card_controller import (
    router as update_router,
)

credit_card_routes = APIRouter(prefix="/api/credit-cards", tags=["credit-cards"])

# Include all controller routers
credit_card_routes.include_router(create_router)
credit_card_routes.include_router(find_router)
credit_card_routes.include_router(update_router)
credit_card_routes.include_router(delete_router)
