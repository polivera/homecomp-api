from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.category.domain.contracts.infrastructure import CategoryRepositoryContract
from app.context.category.domain.dto import CategoryDTO
from app.context.category.domain.exceptions import (
    CategoryDatabaseError,
    CategoryMapperError,
    CategoryNameAlreadyExistError,
)
from app.context.category.domain.value_objects import CategoryID, CategoryName, CategoryUserID
from app.context.category.infrastructure.mappers import CategoryMapper
from app.context.category.infrastructure.models import CategoryModel


class CategoryRepository(CategoryRepositoryContract):
    """Repository for category database operations"""

    def __init__(self, db: AsyncSession):
        self._db = db

    async def save_category(self, category: CategoryDTO) -> CategoryDTO:
        """Create a new category"""
        try:
            model = CategoryMapper.to_model(category)
            self._db.add(model)
            await self._db.commit()
            await self._db.refresh(model)
            return CategoryMapper.to_dto_or_fail(model)
        except IntegrityError as e:
            await self._db.rollback()
            if "unique" in str(e).lower() or "duplicate" in str(e).lower():
                raise CategoryNameAlreadyExistError(
                    f"Category name '{category.name.value}' already exists for this user"
                ) from e
            raise CategoryDatabaseError(f"Database integrity error: {str(e)}") from e
        except CategoryMapperError as e:
            await self._db.rollback()
            raise e
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise CategoryDatabaseError(f"Database error while saving category: {str(e)}") from e

    async def find_category(
        self,
        category_id: CategoryID | None = None,
        user_id: CategoryUserID | None = None,
        name: CategoryName | None = None,
    ) -> CategoryDTO | None:
        """Find a category by ID or by user_id and name"""
        try:
            stmt = select(CategoryModel).where(CategoryModel.deleted_at.is_(None))

            if category_id:
                stmt = stmt.where(CategoryModel.id == category_id.value)
            if user_id:
                stmt = stmt.where(CategoryModel.user_id == user_id.value)
            if name:
                stmt = stmt.where(CategoryModel.name == name.value)

            result = await self._db.execute(stmt)
            model = result.scalar_one_or_none()
            return CategoryMapper.to_dto(model)
        except SQLAlchemyError as e:
            raise CategoryDatabaseError(f"Database error while finding category: {str(e)}") from e

    async def find_user_categories(
        self,
        user_id: CategoryUserID,
        category_id: CategoryID | None = None,
        name: CategoryName | None = None,
        only_active: bool | None = True,
    ) -> list[CategoryDTO] | None:
        """Find user categories always filtering by user_id"""
        try:
            stmt = select(CategoryModel).where(CategoryModel.user_id == user_id.value)

            if only_active:
                stmt = stmt.where(CategoryModel.deleted_at.is_(None))

            if category_id:
                stmt = stmt.where(CategoryModel.id == category_id.value)
            if name:
                stmt = stmt.where(CategoryModel.name.ilike(f"%{name.value}%"))

            stmt = stmt.order_by(CategoryModel.name)

            result = await self._db.execute(stmt)
            models = result.scalars().all()

            if not models:
                return None

            return [CategoryMapper.to_dto_or_fail(model) for model in models]
        except CategoryMapperError as e:
            raise e
        except SQLAlchemyError as e:
            raise CategoryDatabaseError(f"Database error while finding user categories: {str(e)}") from e

    async def find_user_category_by_id(
        self,
        user_id: CategoryUserID,
        category_id: CategoryID,
        only_active: bool | None = True,
    ) -> CategoryDTO | None:
        """Find a specific category by ID for a user"""
        try:
            stmt = select(CategoryModel).where(
                CategoryModel.id == category_id.value, CategoryModel.user_id == user_id.value
            )

            if only_active:
                stmt = stmt.where(CategoryModel.deleted_at.is_(None))

            result = await self._db.execute(stmt)
            model = result.scalar_one_or_none()
            return CategoryMapper.to_dto(model)
        except SQLAlchemyError as e:
            raise CategoryDatabaseError(
                f"Database error while finding category by ID: {str(e)}"
            ) from e

    async def update_category(self, category: CategoryDTO) -> CategoryDTO:
        """Update an existing category"""
        if category.category_id is None:
            raise ValueError("Cannot update category without ID")

        try:
            stmt = (
                update(CategoryModel)
                .where(
                    CategoryModel.id == category.category_id.value,
                    CategoryModel.user_id == category.user_id.value,
                    CategoryModel.deleted_at.is_(None),
                )
                .values(
                    name=category.name.value,
                    color=category.color.value,
                )
                .returning(CategoryModel)
            )

            result = await self._db.execute(stmt)
            await self._db.commit()
            model = result.scalar_one_or_none()

            if model is None:
                raise CategoryDatabaseError("Category not found or already deleted")

            return CategoryMapper.to_dto_or_fail(model)
        except IntegrityError as e:
            await self._db.rollback()
            if "unique" in str(e).lower() or "duplicate" in str(e).lower():
                raise CategoryNameAlreadyExistError(
                    f"Category name '{category.name.value}' already exists for this user"
                ) from e
            raise CategoryDatabaseError(f"Database integrity error: {str(e)}") from e
        except CategoryMapperError as e:
            await self._db.rollback()
            raise e
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise CategoryDatabaseError(f"Database error while updating category: {str(e)}") from e

    async def delete_category(self, category_id: CategoryID, user_id: CategoryUserID) -> bool:
        """Soft delete a category"""
        try:
            stmt = (
                update(CategoryModel)
                .where(
                    CategoryModel.id == category_id.value,
                    CategoryModel.user_id == user_id.value,
                    CategoryModel.deleted_at.is_(None),
                )
                .values(deleted_at=datetime.now(UTC))
                .returning(CategoryModel.id)
            )

            result = await self._db.execute(stmt)
            await self._db.commit()
            deleted_id = result.scalar_one_or_none()

            return deleted_id is not None
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise CategoryDatabaseError(f"Database error while deleting category: {str(e)}") from e
