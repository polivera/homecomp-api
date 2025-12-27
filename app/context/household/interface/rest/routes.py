from fastapi import APIRouter

from app.context.household.interface.rest.controllers import create_household_router

household_routes = APIRouter(prefix="/api/households", tags=["households"])

# Include all household-related routes
household_routes.include_router(create_household_router)
