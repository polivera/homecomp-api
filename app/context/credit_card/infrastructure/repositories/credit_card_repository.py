from typing import Any, cast

from sqlalchemy import select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.credit_card.domain.contracts.infrastructure import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.dto import CreditCardDTO
from app.context.credit_card.domain.exceptions import (
    CreditCardDatabaseError,
    CreditCardNameAlreadyExistError,
    CreditCardNotFoundError,
)
from app.context.credit_card.domain.value_objects import (
    CreditCardDeletedAt,
    CreditCardID,
    CreditCardName,
    CreditCardUserID,
)
from app.context.credit_card.infrastructure.mappers import CreditCardMapper
from app.context.credit_card.infrastructure.models import CreditCardModel


class CreditCardRepository(CreditCardRepositoryContract):
    """Repository implementation for credit card operations"""

    def __init__(self, db: AsyncSession):
        self._db = db

    async def save_credit_card(self, card: CreditCardDTO) -> CreditCardDTO:
        """Create a new credit card"""
        try:
            model = CreditCardMapper.to_model(card)
            self._db.add(model)
            await self._db.commit()
            await self._db.refresh(model)
            return CreditCardMapper.to_dto_or_fail(model)
        except IntegrityError as e:
            await self._db.rollback()
            raise CreditCardNameAlreadyExistError(
                f"Credit card with name '{card.name.value}' already exists for this user"
            ) from e
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise CreditCardDatabaseError(f"Database error while saving credit card: {str(e)}") from e

    async def find_credit_card(
        self,
        card_id: CreditCardID | None = None,
        user_id: CreditCardUserID | None = None,
        name: CreditCardName | None = None,
        only_active: bool | None = True,
    ) -> CreditCardDTO | None:
        """Find a credit card by ID or by user_id and name (admin/unrestricted usage)"""
        try:
            stmt = select(CreditCardModel)
            if only_active:
                stmt = stmt.where(CreditCardModel.deleted_at.is_(None))

            if card_id is not None:
                stmt = stmt.where(CreditCardModel.id == card_id.value)
            elif user_id is not None and name is not None:
                stmt = stmt.where(
                    CreditCardModel.user_id == user_id.value,
                    CreditCardModel.name == name.value,
                )
            else:
                raise ValueError("Must provide either card_id or both user_id and name")

            result = await self._db.execute(stmt)
            model = result.scalar_one_or_none()

            return CreditCardMapper.to_dto(model) if model else None
        except SQLAlchemyError as e:
            raise CreditCardDatabaseError(f"Database error while finding credit card: {str(e)}") from e

    async def find_user_credit_cards(
        self,
        user_id: CreditCardUserID,
        card_id: CreditCardID | None = None,
        name: CreditCardName | None = None,
        only_active: bool | None = True,
    ) -> list[CreditCardDTO] | None:
        """Find user credit cards always filtering by user_id (for user-scoped queries)"""
        try:
            stmt = select(CreditCardModel).where(CreditCardModel.user_id == user_id.value)
            if only_active:
                stmt = stmt.where(CreditCardModel.deleted_at.is_(None))

            if card_id is not None:
                stmt = stmt.where(CreditCardModel.id == card_id.value)
            else:
                if name is not None:
                    stmt = stmt.where(CreditCardModel.name.like(f"%{name.value}%"))

            models = (await self._db.execute(stmt)).scalars()
            return [CreditCardMapper.to_dto_or_fail(model) for model in models] if models else []
        except SQLAlchemyError as e:
            raise CreditCardDatabaseError(f"Database error while finding user credit cards: {str(e)}") from e

    async def find_user_credit_card_by_id(
        self,
        user_id: CreditCardUserID,
        card_id: CreditCardID,
        only_active: bool | None = True,
    ) -> CreditCardDTO | None:
        """Find a specific credit card by ID for a user"""
        try:
            stmt = select(CreditCardModel).where(
                CreditCardModel.id == card_id.value,
                CreditCardModel.user_id == user_id.value,
            )
            if only_active:
                stmt = stmt.where(CreditCardModel.deleted_at.is_(None))

            model = (await self._db.execute(stmt)).scalar_one_or_none()
            return CreditCardMapper.to_dto(model)
        except SQLAlchemyError as e:
            raise CreditCardDatabaseError(f"Database error while finding credit card by ID: {str(e)}") from e

    async def update_credit_card(self, card: CreditCardDTO) -> CreditCardDTO:
        """Update an existing credit card"""
        if card.credit_card_id is None:
            raise ValueError("Credit Card ID not given")

        try:
            stmt = (
                update(CreditCardModel)
                .where(
                    CreditCardModel.id == card.credit_card_id.value,
                    CreditCardModel.deleted_at.is_(None),
                )
                .values(
                    name=card.name.value,
                    limit=card.limit.value,
                )
            )
            if card.used is not None:
                stmt = stmt.values(used=card.used.value)

            result = cast(CursorResult[Any], await self._db.execute(stmt))
            if result.rowcount == 0:
                raise CreditCardNotFoundError(
                    f"Credit card with ID {card.credit_card_id.value} not found or already deleted"
                )

            await self._db.commit()

            return card
        except IntegrityError as e:
            await self._db.rollback()
            raise CreditCardNameAlreadyExistError(
                f"Credit card with name '{card.name.value}' already exists for this user"
            ) from e
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise CreditCardDatabaseError(f"Database error while updating credit card: {str(e)}") from e

    async def delete_credit_card(self, card_id: CreditCardID, user_id: CreditCardUserID) -> bool:
        """Soft delete a credit card"""
        try:
            # Verify card exists and user owns it
            card = await self.find_credit_card(card_id=card_id)
            if not card or card.user_id.value != user_id.value:
                return False

            # Soft delete: set deleted_at timestamp
            stmt = (
                update(CreditCardModel)
                .where(
                    CreditCardModel.id == card_id.value,
                    CreditCardModel.user_id == user_id.value,
                    CreditCardModel.deleted_at.is_(None),
                )
                .values(deleted_at=CreditCardDeletedAt.now().value)
            )

            result = cast(CursorResult[Any], await self._db.execute(stmt))
            await self._db.commit()

            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise CreditCardDatabaseError(f"Database error while deleting credit card: {str(e)}") from e
        except Exception as e:
            await self._db.rollback()
            raise CreditCardDatabaseError(f"Unexpected error while deleting credit card: {str(e)}") from e
