from typing import Annotated

from fastapi import APIRouter, Depends

from app.context.credit_card.application.queries import FindCreditCardsByUserQuery
from app.context.credit_card.interface.schemas.credit_card_response import (
    CreditCardResponse,
)
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/cards")


@router.get("", response_model=list[CreditCardResponse])
async def get_credit_cards(
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Get all credit cards for the current user"""
    logger = app_container.logger
    handler = app_container.get_find_credit_cards_by_user_handler()

    logger.info("Get all credit cards for user request", user_id=user_id)

    query = FindCreditCardsByUserQuery(user_id=user_id)

    results = await handler.handle(query)

    logger.info("Credit cards retrieved successfully", user_id=user_id, count=len(results))

    return [
        CreditCardResponse(
            credit_card_id=result.credit_card_id,
            user_id=result.user_id,
            account_id=result.account_id,
            name=result.name,
            currency=result.currency,
            limit=result.limit,
            used=result.used,
        )
        for result in results
    ]
