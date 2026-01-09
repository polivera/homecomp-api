from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryResponse:
    category_id: int
    user_id: int
    name: str
    color: str
