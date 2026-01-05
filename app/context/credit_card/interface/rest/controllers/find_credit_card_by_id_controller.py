from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.credit_card.application.queries import FindCreditCardByIdQuery
from app.context.credit_card.interface.schemas.credit_card_response import (
    CreditCardResponse,
)
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/cards")


@router.get("/{credit_card_id}", response_model=CreditCardResponse)
async def get_credit_card(
    credit_card_id: int,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Get a credit card by ID"""
    logger = app_container.logger
    handler = app_container.get_find_credit_card_by_id_handler()

    logger.info("Get credit card by ID request", user_id=user_id, credit_card_id=credit_card_id)

    query = FindCreditCardByIdQuery(
        credit_card_id=credit_card_id,
        user_id=user_id,
    )

    result = await handler.handle(query)

    if not result:
        logger.warning("Credit card not found", user_id=user_id, credit_card_id=credit_card_id)
        raise HTTPException(
            status_code=404,
            detail=f"Credit card with ID {credit_card_id} not found",
        )

    logger.info("Credit card retrieved successfully", user_id=user_id, credit_card_id=credit_card_id)

    return CreditCardResponse(
        credit_card_id=result.credit_card_id,
        user_id=result.user_id,
        account_id=result.account_id,
        name=result.name,
        currency=result.currency,
        limit=result.limit,
        used=result.used,
    )
