from abc import ABC

from app.context.user.domain.value_objects import Email, Password


class LoginServiceContract(ABC):
    # TODO: create return dto
    async def handle(self, email: Email, password: Password):
        pass
