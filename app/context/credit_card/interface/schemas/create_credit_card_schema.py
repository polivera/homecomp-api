from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateCreditCardRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=3, max_length=100, description="Credit card name")
    account_id: int = Field(..., description="Account associated with the credit card")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (ISO 4217)")
    limit: float = Field(..., gt=0, description="Credit card limit")

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        """Ensure currency is uppercase and exactly 3 characters"""
        return v.upper()
