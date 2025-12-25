from pydantic import BaseModel, ConfigDict


class CreateAccountRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    currency: str
    balance: float
