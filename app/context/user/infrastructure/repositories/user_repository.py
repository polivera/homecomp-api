from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user.domain.contracts.infrastrutcure import UserRepositoryContract
from app.context.user.domain.dto import UserDTO
from app.context.user.domain.value_objects import Email, Password, UserID


class UserRepository(UserRepositoryContract):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_user(
        self, user_id: Optional[UserID] = None, email: Optional[Email] = None
    ) -> Optional[UserDTO]:
        print("----------------------------------------------------")
        print("Entering in the repository")
        print(user_id.value if user_id is not None else "no id sent")
        print(email.value if email is not None else "no email sent")
        print("----------------------------------------------------")
        return UserDTO(
            user_id=UserID(1),
            email=Email("test@test.com"),
            password=Password.from_hash(
                "$argon2id$v=19$m=65536,t=3,p=4$BtkhPdaq4kwywhCm5+SDRw$gqds7qYNWVrWd48HS/eGbe+FZrUu9ndZp98pK2zPMgU"
            ),
        )
