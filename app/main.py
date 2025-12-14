from fastapi import FastAPI
from contextlib import asynccontextmanager
from .infrastructure.database import async_engine
from .context.auth.interface.rest import auth_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables (or use Alembic for migrations)
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    yield  # Application runs

    # Shutdown: Close connection pool
    await async_engine.dispose()


app = FastAPI(
    title="Homecomp API",
    description="API for Homecomp",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth_routes)


@app.get("/")
async def root():
    return {"message": "Welcome to Homecomp API"}
