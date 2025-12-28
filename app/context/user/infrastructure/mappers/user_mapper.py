from dataclasses import dataclass
from typing import Optional

from app.context.user.domain.dto.user_dto import UserDTO
from app.context.user.domain.value_objects import Email, Password, UserDeletedAt, UserID
from app.context.user.infrastructure.models.user_model import UserModel


@dataclass(frozen=True)
class UserMapper:
    @staticmethod
    def toDTO(model: Optional[UserModel]) -> Optional[UserDTO]:
        if model is None:
            return None

        return UserDTO(
            user_id=UserID(model.id),
            email=Email(model.email),
            password=Password.from_hash(model.password),
            deleted_at=UserDeletedAt.from_optional(model.deleted_at),
        )
