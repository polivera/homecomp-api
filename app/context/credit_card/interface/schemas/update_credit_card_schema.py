from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UpdateCreditCardRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: Optional[str] = Field(
        None, min_length=3, max_length=100, description="Credit card name"
    )
    limit: Optional[float] = Field(None, gt=0, description="Credit card limit")
    used: Optional[float] = Field(None, ge=0, description="Credit card used amount")
