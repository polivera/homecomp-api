from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.context.auth.interface.rest import auth_routes

app = FastAPI(
    title="Homecomp API",
    description="API for Homecomp",
    version="0.1.0",
    # lifespan=lifespan,
)

app.include_router(auth_routes)


@app.get("/")
async def root():
    return {"message": "Welcome to Homecomp API"}
