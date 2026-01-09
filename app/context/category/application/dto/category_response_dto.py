from dataclasses import dataclass

from app.context.category.domain.dto import CategoryDTO


@dataclass(frozen=True)
class CategoryResponseDTO:
    """Application layer DTO for category responses"""

    category_id: int
    user_id: int
    name: str
    color: str

    @classmethod
    def from_domain_dto(cls, domain_dto: CategoryDTO) -> "CategoryResponseDTO":
        if domain_dto.category_id is None:
            raise ValueError("Cannot create CategoryResponseDTO from domain DTO without category_id")

        return cls(
            category_id=domain_dto.category_id.value,
            user_id=domain_dto.user_id.value,
            name=domain_dto.name.value,
            color=domain_dto.color.value,
        )
