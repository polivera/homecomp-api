import asyncio

from app.context.user.application.handlers import FindUserHandler
from app.context.user.application.queries import FindUserQuery
from app.context.user.infrastructure.repositories import UserRepository
from app.shared.infrastructure.database import AsyncSessionLocal


async def main():
    async with AsyncSessionLocal() as session:
        # Manually construct the dependencies
        user_repo = UserRepository(session)
        handler = FindUserHandler(user_repo)

        # Example 1: Find by email
        query = FindUserQuery(user_id=None, email="test@example.com")
        result = await handler.handle(query)
        print(f"Result: {result}")

        # Example 2: Find by id
        # query = FindUserQuery(id=1, email=None, password=None)
        # result = await handler.handle(query)
        # print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
