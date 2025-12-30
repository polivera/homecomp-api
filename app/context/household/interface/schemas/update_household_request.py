from pydantic import BaseModel, ConfigDict


class UpdateHouseholdRequest(BaseModel):
    """Request schema for updating household"""

    model_config = ConfigDict(frozen=True)
    name: str
