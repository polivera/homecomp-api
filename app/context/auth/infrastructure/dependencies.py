from app.context.auth.application.contracts import LoginHandlerContract
from app.context.auth.application.handlers import LoginHandler


def get_login_handler() -> LoginHandlerContract:
    """
    Login handler dependency
    """
    return LoginHandler()
