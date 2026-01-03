"""REST controllers for occurrence endpoints"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.reminder.application.commands import PayReminderOccurrenceCommand
from app.context.reminder.application.contracts import (
    ListOccurrencesHandlerContract,
    PayReminderOccurrenceHandlerContract,
)
from app.context.reminder.application.dto import ListOccurrencesErrorCode, PayReminderOccurrenceErrorCode
from app.context.reminder.application.queries import ListOccurrencesQuery
from app.context.reminder.infrastructure.dependencies import (
    get_list_occurrences_handler,
    get_pay_reminder_occurrence_handler,
)
from app.context.reminder.interface.schemas import (
    OccurrenceListResponse,
    OccurrenceResponse,
    PayReminderOccurrenceResponse,
)
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


@router.post("/{occurrence_id}/pay", response_model=PayReminderOccurrenceResponse, status_code=200)
async def pay_reminder_occurrence(
    occurrence_id: int,
    handler: Annotated[PayReminderOccurrenceHandlerContract, Depends(get_pay_reminder_occurrence_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """
    Mark a reminder occurrence as paid

    This will:
    - Mark the occurrence as completed
    - Create an entry record for the payment
    - Return the created entry_id
    """

    command = PayReminderOccurrenceCommand(occurrence_id=occurrence_id, user_id=user_id)

    result = await handler.handle(command)

    # Map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            PayReminderOccurrenceErrorCode.OCCURRENCE_NOT_FOUND: 404,
            PayReminderOccurrenceErrorCode.OCCURRENCE_NOT_BELONGS_TO_USER: 403,
            PayReminderOccurrenceErrorCode.OCCURRENCE_ALREADY_PAID: 409,
            PayReminderOccurrenceErrorCode.UNEXPECTED_ERROR: 500,
        }
        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return success response
    return PayReminderOccurrenceResponse(paid=result.paid, entry_id=result.entry_id)
