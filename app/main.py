from fastapi import FastAPI
from .context.auth.interface.rest import auth_routes

app = FastAPI(title="Homecomp API", description="API for Homecomp", version="0.1.0")

app.include_router(auth_routes)


@app.get("/")
async def root():
    return {"message": "Welcome to Homecomp API"}
