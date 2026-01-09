from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field, field_validator


@dataclass(frozen=True)
class CreateCategoryResponse:
    category_id: int
    name: str
    color: str


class CreateCategoryRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    color: str = Field(..., min_length=7, max_length=7, description="Hex color code (e.g., #FF5733)")

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str) -> str:
        """Ensure color is a valid hex code"""
        if not v.startswith("#"):
            raise ValueError("Color must start with #")
        try:
            int(v[1:], 16)
        except ValueError:
            raise ValueError("Color must be a valid hex color code (e.g., #FF5733)")
        return v.upper()
