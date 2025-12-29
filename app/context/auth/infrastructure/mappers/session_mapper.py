from dataclasses import dataclass

from app.context.auth.domain.dto import SessionDTO
from app.context.auth.domain.value_objects import (
    AuthUserID,
    FailedLoginAttempts,
    SessionToken,
)
from app.context.auth.domain.value_objects.blocked_time import BlockedTime
from app.context.auth.infrastructure.models import SessionModel


@dataclass(frozen=True)
class SessionMapper:
    @staticmethod
    def toDTO(model: SessionModel | None) -> SessionDTO | None:
        if model is None:
            return None

        return SessionDTO(
            user_id=AuthUserID(model.user_id),
            token=SessionToken.from_string(model.token) if model.token else None,
            failed_attempts=FailedLoginAttempts(model.failed_attempts),
            blocked_until=BlockedTime(model.blocked_until)
            if model.blocked_until is not None
            else None,
        )

    @staticmethod
    def toModel(dto: SessionDTO) -> SessionModel:
        return SessionModel(
            user_id=dto.user_id.value,
            token=dto.token.value if dto.token else None,
            failed_attempts=dto.failed_attempts.value,
            blocked_until=dto.blocked_until,
        )
