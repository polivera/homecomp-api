from fastapi import APIRouter

from app.context.household.interface.rest.controllers import (
    accept_invite_router,
    create_household_router,
    decline_invite_router,
    delete_household_router,
    get_household_router,
    invite_user_router,
    list_household_invites_router,
    list_user_households_router,
    list_user_pending_invites_router,
    remove_member_router,
    update_household_router,
)

household_routes = APIRouter(prefix="/api/households", tags=["households"])

# Include all household-related routes
household_routes.include_router(create_household_router)
household_routes.include_router(get_household_router)
household_routes.include_router(list_user_households_router)
household_routes.include_router(update_household_router)
household_routes.include_router(delete_household_router)
household_routes.include_router(invite_user_router)
household_routes.include_router(accept_invite_router)
household_routes.include_router(decline_invite_router)
household_routes.include_router(remove_member_router)
household_routes.include_router(list_household_invites_router)
household_routes.include_router(list_user_pending_invites_router)
