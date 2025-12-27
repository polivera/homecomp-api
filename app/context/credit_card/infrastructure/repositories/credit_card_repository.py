from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.dto.credit_card_dto import CreditCardDTO
from app.context.credit_card.domain.exceptions import (
    CreditCardCreationError,
    CreditCardNameAlreadyExistError,
    CreditCardNotFoundError,
    CreditCardRepositoryInvalidParametersError,
    CreditCardUpdateError,
    CreditCardUpdateWithoutIdError,
)
from app.context.credit_card.domain.value_objects.credit_card_id import CreditCardID
from app.context.credit_card.domain.value_objects.credit_card_name import (
    CreditCardName,
)
from app.context.credit_card.infrastructure.mappers.credit_card_mapper import (
    CreditCardMapper,
)
from app.context.credit_card.infrastructure.models.credit_card_model import (
    CreditCardModel,
)
from app.context.user.domain.value_objects.user_id import UserID


class CreditCardRepository(CreditCardRepositoryContract):
    """Repository for credit card persistence operations"""

    def __init__(self, db: AsyncSession):
        self._db = db

    async def save_credit_card(self, card: CreditCardDTO) -> CreditCardDTO:
        """Create a new credit card in the database"""
        model = CreditCardMapper.toModel(card)

        self._db.add(model)

        try:
            await self._db.commit()
            await self._db.refresh(model)
        except IntegrityError as e:
            await self._db.rollback()
            if "uq_credit_cards_user_id_name" in str(e.orig):
                raise CreditCardNameAlreadyExistError(
                    f"Credit card with name '{card.name.value}' already exists for this user"
                ) from e
            raise CreditCardCreationError(f"Failed to create credit card: {str(e)}") from e

        return CreditCardMapper.toDTO(model)

    async def find_credit_card(
        self,
        card_id: Optional[CreditCardID] = None,
        user_id: Optional[UserID] = None,
        name: Optional[CreditCardName] = None,
    ) -> Optional[CreditCardDTO]:
        """Find a credit card by ID or by user_id and name"""
        stmt = select(CreditCardModel).where(CreditCardModel.deleted_at.is_(None))

        if card_id is not None:
            stmt = stmt.where(CreditCardModel.id == card_id.value)
        elif user_id is not None and name is not None:
            stmt = stmt.where(
                CreditCardModel.user_id == user_id.value,
                CreditCardModel.name == name.value,
            )
        else:
            raise CreditCardRepositoryInvalidParametersError(
                "Must provide either card_id or both user_id and name"
            )

        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()

        return CreditCardMapper.toDTO(model) if model else None

    async def find_credit_cards_by_user(self, user_id: UserID) -> list[CreditCardDTO]:
        """Find all non-deleted credit cards for a user"""
        stmt = select(CreditCardModel).where(
            CreditCardModel.user_id == user_id.value,
            CreditCardModel.deleted_at.is_(None),
        )

        result = await self._db.execute(stmt)
        models = result.scalars().all()

        return [CreditCardMapper.toDTO(model) for model in models]

    async def update_credit_card(self, card: CreditCardDTO) -> CreditCardDTO:
        """Update an existing credit card"""
        if card.credit_card_id is None:
            raise CreditCardUpdateWithoutIdError("Cannot update credit card without an ID")

        stmt = (
            update(CreditCardModel)
            .where(
                CreditCardModel.id == card.credit_card_id.value,
                CreditCardModel.deleted_at.is_(None),
            )
            .values(
                name=card.name.value,
                limit=card.limit.value,
                used=card.used.value,
            )
        )

        try:
            result = await self._db.execute(stmt)
            await self._db.commit()

            if result.rowcount == 0:
                raise CreditCardNotFoundError(
                    f"Credit card with ID {card.credit_card_id.value} not found"
                )

            # Fetch and return updated card
            return await self.find_credit_card(card_id=card.credit_card_id)

        except IntegrityError as e:
            await self._db.rollback()
            if "uq_credit_cards_user_id_name" in str(e.orig):
                raise CreditCardNameAlreadyExistError(
                    f"Credit card with name '{card.name.value}' already exists for this user"
                ) from e
            raise CreditCardUpdateError(f"Failed to update credit card: {str(e)}") from e

    async def delete_credit_card(self, card_id: CreditCardID, user_id: UserID) -> bool:
        """Soft delete a credit card"""
        # Verify the card exists and belongs to the user
        card = await self.find_credit_card(card_id=card_id)
        if not card or card.user_id.value != user_id.value:
            return False

        stmt = (
            update(CreditCardModel)
            .where(
                CreditCardModel.id == card_id.value,
                CreditCardModel.user_id == user_id.value,
                CreditCardModel.deleted_at.is_(None),
            )
            .values(deleted_at=datetime.utcnow())
        )

        result = await self._db.execute(stmt)
        await self._db.commit()

        return result.rowcount > 0
