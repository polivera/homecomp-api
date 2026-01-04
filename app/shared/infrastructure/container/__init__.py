from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.infrastructure.database import get_db

from .app_container import ApplicationContainer


def get_fastapi_app_container(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApplicationContainer:
    return ApplicationContainer(db)


__all__ = ["ApplicationContainer", "get_fastapi_app_container"]
