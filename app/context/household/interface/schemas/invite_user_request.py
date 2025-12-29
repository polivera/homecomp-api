from pydantic import BaseModel, ConfigDict, Field


class InviteUserRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    invitee_user_id: int = Field(..., gt=0, description="User ID of the person being invited")
    role: str = Field(
        ..., description="Role to assign (owner, admin, participant)", pattern="^(owner|admin|participant)$"
    )
