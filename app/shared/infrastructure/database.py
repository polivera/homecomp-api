from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_NAME = getenv("DB_NAME")

DATABASE_URL = getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

echo_queries = getenv("APP_ENV", "prod") == "debug"

async_engine = create_async_engine(
    DATABASE_URL,
    echo=echo_queries,  # Log SQL queries (disable in production)
    pool_size=10,  # Keep 10 persistent connections
    max_overflow=20,  # Allow 20 more if needed
    pool_pre_ping=True,  # Verify connection is alive before using
    pool_recycle=3600,  # Recycle connections after 1 hour
)

AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
