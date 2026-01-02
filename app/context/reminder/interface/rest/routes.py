"""Router configuration for reminder context"""

from fastapi import APIRouter

from .controllers import occurrence_router, reminder_router

# Create main router for reminder context
reminder_context_router = APIRouter(prefix="/api/v1")

# Include all sub-routers
reminder_context_router.include_router(reminder_router)
reminder_context_router.include_router(occurrence_router)
