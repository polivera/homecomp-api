from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.entry.application.commands import DeleteEntryCommand
from app.context.entry.application.contracts import DeleteEntryHandlerContract
from app.context.entry.application.dto import DeleteEntryErrorCode
from app.context.entry.infrastructure.dependencies import get_delete_entry_handler
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/entries")


@router.delete("/{entry_id}", status_code=204)
async def delete_entry(
    entry_id: int,
    handler: Annotated[DeleteEntryHandlerContract, Depends(get_delete_entry_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
):
    """Delete an entry (hard delete)"""
    logger.info("Delete entry request", user_id=user_id, entry_id=entry_id)

    command = DeleteEntryCommand(entry_id=entry_id, user_id=user_id)
    result = await handler.handle(command)

    if result.error_code:
        status_code_map = {
            DeleteEntryErrorCode.NOT_FOUND: 404,
            DeleteEntryErrorCode.UNEXPECTED_ERROR: 500,
        }

        status_code = status_code_map.get(result.error_code, 500)

        if status_code == 404:
            logger.warning("Entry deletion failed - not found", user_id=user_id, entry_id=entry_id)
        else:
            logger.error("Entry deletion failed", user_id=user_id, entry_id=entry_id, error=result.error_message)

        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return 204 No Content on success
    logger.info("Entry deleted successfully", user_id=user_id, entry_id=entry_id)
    return
