from fastapi import Depends

from app.context.auth.application.contracts import LoginHandlerContract
from app.context.auth.application.handlers import LoginHandler
from app.context.auth.domain.contracts import LoginServiceContract
from app.context.auth.domain.services import LoginService
from app.context.user.infrastructure.dependency import (
    get_find_user_query_handler,
)


def get_login_service(
    userQueryHandler=Depends(get_find_user_query_handler),
) -> LoginServiceContract:
    return LoginService(userQueryHandler)


def get_login_handler(
    user_query_handler=Depends(get_find_user_query_handler),
) -> LoginHandlerContract:
    """
    Login handler dependency
    """
    return LoginHandler(user_query_handler)
