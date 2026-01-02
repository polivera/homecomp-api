from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateAccountRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=1, max_length=100, description="Account name")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (ISO 4217)")
    balance: float = Field(..., description="Initial account balance")

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        """Ensure currency is uppercase and exactly 3 characters"""
        return v.upper()
