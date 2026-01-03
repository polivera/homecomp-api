"""Router configuration for reminder context"""

from fastapi import APIRouter

from .controllers import (
    create_reminder_router,
    delete_reminder_router,
    find_reminder_router,
    occurrence_router,
    update_reminder_router,
)

# Create main router for reminder context
reminder_context_router = APIRouter(prefix="/api")

# Include all sub-routers
reminder_context_router.include_router(create_reminder_router)
reminder_context_router.include_router(find_reminder_router)
reminder_context_router.include_router(update_reminder_router)
reminder_context_router.include_router(delete_reminder_router)
reminder_context_router.include_router(occurrence_router)
