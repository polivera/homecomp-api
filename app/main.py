from os import getenv

from fastapi import FastAPI

from app.context.auth.interface.rest import auth_routes
from app.context.credit_card.interface.rest import credit_card_routes
from app.context.household.interface.rest import household_routes
from app.context.user_account.interface.rest import user_account_routes
from app.shared.infrastructure.logging.config import configure_structlog

# Configure structlog (skip in test environment)
if getenv("APP_ENV") != "test":
    use_json = getenv("APP_ENV") == "production"
    configure_structlog(use_json=use_json)

app = FastAPI(
    title="Homecomp API",
    description="API for Homecomp",
    version="0.1.0",
    # lifespan=lifespan,
)

app.include_router(auth_routes)
app.include_router(user_account_routes)
app.include_router(credit_card_routes)
app.include_router(household_routes)


@app.get("/")
async def root():
    return {"message": "Welcome to Homecomp API"}
