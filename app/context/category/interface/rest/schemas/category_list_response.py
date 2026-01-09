from dataclasses import dataclass

from app.context.category.interface.rest.schemas.category_response import CategoryResponse


@dataclass(frozen=True)
class CategoryListResponse:
    categories: list[CategoryResponse]
