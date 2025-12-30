from typing import Annotated

from fastapi import APIRouter, Depends

from app.context.credit_card.application.contracts import (
    FindCreditCardsByUserHandlerContract,
)
from app.context.credit_card.application.queries import FindCreditCardsByUserQuery
from app.context.credit_card.infrastructure.dependencies import (
    get_find_credit_cards_by_user_handler,
)
from app.context.credit_card.interface.schemas.credit_card_response import (
    CreditCardResponse,
)
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/cards")


@router.get("", response_model=list[CreditCardResponse])
async def get_credit_cards(
    handler: Annotated[FindCreditCardsByUserHandlerContract, Depends(get_find_credit_cards_by_user_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
):
    """Get all credit cards for the current user"""
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
