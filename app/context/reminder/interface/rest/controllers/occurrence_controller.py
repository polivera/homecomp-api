"""REST controllers for occurrence endpoints"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.reminder.application.contracts import ListOccurrencesHandlerContract
from app.context.reminder.application.dto import ListOccurrencesErrorCode
from app.context.reminder.application.queries import ListOccurrencesQuery
from app.context.reminder.infrastructure.dependencies import get_list_occurrences_handler
from app.context.reminder.interface.rest.schemas import OccurrenceListResponse, OccurrenceResponse
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/occurrences", tags=["occurrences"])


@router.get("", response_model=OccurrenceListResponse)
async def list_occurrences(
    handler: Annotated[ListOccurrencesHandlerContract, Depends(get_list_occurrences_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    reminder_id: int | None = None,
):
    """
    List occurrences for the authenticated user

    If reminder_id is provided, returns occurrences for that specific reminder.
    Otherwise, returns all pending occurrences for the user.
    """

    query = ListOccurrencesQuery(user_id=user_id, reminder_id=reminder_id)

    result = await handler.handle(query)

    # Map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            ListOccurrencesErrorCode.UNEXPECTED_ERROR: 500,
        }
        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Convert to response
    occurrences = [
        OccurrenceResponse(
            id=item.occurrence_id,
            reminder_id=item.reminder_id,
            scheduled_date=item.scheduled_date,
            amount=item.amount,
            status=item.status,
            entry_id=item.entry_id,
            description=item.description,
            entry_type=item.entry_type,
            currency=item.currency,
            category_id=item.category_id,
        )
        for item in result.occurrences
    ]

    return OccurrenceListResponse(occurrences=occurrences)
