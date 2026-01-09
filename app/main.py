from fastapi import FastAPI

from app.context.auth.interface.rest import auth_routes
from app.context.category.interface.rest.routes import category_routes
from app.context.credit_card.interface.rest import credit_card_routes
from app.context.entry.interface.rest import entry_routes
from app.context.household.interface.rest import household_routes
from app.context.reminder.interface.rest.routes import reminder_context_router
from app.context.user_account.interface.rest import user_account_routes
from app.shared.domain.value_objects.shared_app_env import SharedAppEnv
from app.shared.infrastructure.logging.config import configure_structlog

# Configure structlog (skip in test environment)
# if "APP_ENV") != "test":
if not SharedAppEnv.isTest():
    configure_structlog(use_json=SharedAppEnv.isProd())

app = FastAPI(
    title="Homecomp API",
    description="API for Homecomp",
    version="0.1.0",
    # lifespan=lifespan,
)

app.include_router(auth_routes)
app.include_router(user_account_routes)
app.include_router(credit_card_routes)
app.include_router(category_routes)
app.include_router(entry_routes)
app.include_router(household_routes)
app.include_router(reminder_context_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Homecomp API"}
