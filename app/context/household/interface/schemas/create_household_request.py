from pydantic import BaseModel, ConfigDict, Field


class CreateHouseholdRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=1, max_length=100, description="Household name")
