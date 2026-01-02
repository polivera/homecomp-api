from pydantic import BaseModel, ConfigDict, Field, field_validator


class UpdateAccountRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=1, max_length=100)
    currency: str = Field(..., min_length=3, max_length=3)
    balance: float = Field(...)

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        return v.upper()
