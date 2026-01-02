# Controllers export their routers directly in routes.py
from .create_entry_controller import router as create_router
from .delete_entry_controller import router as delete_router
from .find_entry_controller import router as find_router
from .update_entry_controller import router as update_router

__all__ = ["create_router", "find_router", "update_router", "delete_router"]
