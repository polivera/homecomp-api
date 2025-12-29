
from app.context.user.domain.dto.user_dto import UserDTO
from app.context.user.domain.exceptions import UserMapperError
from app.context.user.domain.value_objects import (
    UserDeletedAt,
    UserEmail,
    UserID,
    UserName,
    UserPassword,
)
from app.context.user.infrastructure.models.user_model import UserModel


class UserMapper:
    """Mapper between UserModel (database) and UserDTO (domain)"""

    @staticmethod
    def to_dto(model: UserModel | None) -> UserDTO | None:
        """
        Convert database model to domain DTO.
        Uses from_trusted_source for performance optimization.
        """
        return (
            UserDTO(
                user_id=UserID.from_trusted_source(model.id),
                email=UserEmail.from_trusted_source(model.email),
                password=UserPassword.from_hash(model.password),
                username=UserName.from_trusted_source(model.username)
                if model.username
                else None,
                deleted_at=UserDeletedAt.from_optional(model.deleted_at),
            )
            if model
            else None
        )

    @staticmethod
    def to_dto_or_fail(model: UserModel) -> UserDTO:
        """
        Convert database model to domain DTO.
        Raises UserMapperError if model is None.
        """
        dto = UserMapper.to_dto(model)
        if dto is None:
            raise UserMapperError("User DTO cannot be null")
        return dto

    @staticmethod
    def to_model(dto: UserDTO) -> UserModel:
        """Convert domain DTO to database model"""
        return UserModel(
            id=dto.user_id.value if dto.user_id else None,
            email=dto.email.value,
            password=dto.password.value,
            username=dto.username.value if dto.username else None,
            deleted_at=dto.deleted_at.value if dto.deleted_at else None,
        )
