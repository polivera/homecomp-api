from pydantic import BaseModel, ConfigDict, Field


class UpdateCreditCardRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str | None = Field(None, min_length=3, max_length=100, description="Credit card name")
    limit: float | None = Field(None, gt=0, description="Credit card limit")
    used: float | None = Field(None, ge=0, description="Credit card used amount")
