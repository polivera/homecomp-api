import asyncio

from app.context.user.application.query.find_user_query import FindUserQuery
from app.context.user.infrastructure.repository.user_repository import UserRepository
from app.context.user.application.handler.find_user_handler import FindUserHandler
from app.infrastructure.database import AsyncSessionLocal


async def main():
    async with AsyncSessionLocal() as session:
        # Manually construct the dependencies
        user_repo = UserRepository(session)
        handler = FindUserHandler(user_repo)

        # Example 1: Find by email
        query = FindUserQuery(id=None, email="test@example.com", password=None)
        result = await handler.handle(query)
        print(f"Result: {result}")

        # Example 2: Find by id
        # query = FindUserQuery(id=1, email=None, password=None)
        # result = await handler.handle(query)
        # print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
