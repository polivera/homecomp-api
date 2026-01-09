from app.context.category.domain.dto import CategoryDTO
from app.context.category.domain.exceptions import CategoryMapperError
from app.context.category.domain.value_objects import (
    CategoryColor,
    CategoryDeletedAt,
    CategoryID,
    CategoryName,
    CategoryUserID,
)
from app.context.category.infrastructure.models import CategoryModel


class CategoryMapper:
    """Mapper to convert between CategoryModel and CategoryDTO"""

    @staticmethod
    def to_dto(model: CategoryModel | None) -> CategoryDTO | None:
        """Convert database model to domain DTO"""
        return (
            CategoryDTO(
                category_id=CategoryID.from_trusted_source(model.id),
                user_id=CategoryUserID.from_trusted_source(model.user_id),
                name=CategoryName.from_trusted_source(model.name),
                color=CategoryColor.from_trusted_source(model.color),
                deleted_at=CategoryDeletedAt.from_optional(model.deleted_at),
            )
            if model
            else None
        )

    @staticmethod
    def to_dto_or_fail(model: CategoryModel | None) -> CategoryDTO:
        """
        Convert database model to domain DTO, raising error if model is None

        Raises:
            CategoryMapperError: If model is None
        """
        dto = CategoryMapper.to_dto(model)
        if dto is None:
            raise CategoryMapperError("Cannot map None model to DTO")
        return dto

    @staticmethod
    def to_model(dto: CategoryDTO) -> CategoryModel:
        """Convert domain DTO to database model"""
        return CategoryModel(
            id=dto.category_id.value if dto.category_id is not None else None,
            user_id=dto.user_id.value,
            name=dto.name.value,
            color=dto.color.value,
            deleted_at=dto.deleted_at.value if dto.deleted_at is not None else None,
        )
