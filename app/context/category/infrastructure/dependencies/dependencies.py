from sqlalchemy.ext.asyncio import AsyncSession

from app.context.category.application.contracts import (
    CreateCategoryHandlerContract,
    DeleteCategoryHandlerContract,
    FindCategoriesByUserHandlerContract,
    FindCategoryByIdHandlerContract,
    UpdateCategoryHandlerContract,
)
from app.context.category.domain.contracts.infrastructure import CategoryRepositoryContract
from app.context.category.domain.contracts.services import (
    CreateCategoryServiceContract,
    DeleteCategoryServiceContract,
    FindCategoriesByUserServiceContract,
    FindCategoryByIdServiceContract,
    UpdateCategoryServiceContract,
)
from app.shared.domain.contracts import LoggerContract

# ─────────────────────────────────────────────────────────────────
# COMMAND HANDLERS (Write operations)
# ─────────────────────────────────────────────────────────────────


def create_category_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> CreateCategoryHandlerContract:
    """Factory for CreateCategoryHandler with all dependencies"""
    from app.context.category.application.handlers import CreateCategoryHandler

    service = _get_create_category_service(_get_category_repository(db), logger)
    return CreateCategoryHandler(service, logger)


def update_category_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> UpdateCategoryHandlerContract:
    """Factory for UpdateCategoryHandler with all dependencies"""
    from app.context.category.application.handlers import UpdateCategoryHandler

    service = _get_update_category_service(_get_category_repository(db), logger)
    return UpdateCategoryHandler(service, logger)


def delete_category_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> DeleteCategoryHandlerContract:
    """Factory for DeleteCategoryHandler with all dependencies"""
    from app.context.category.application.handlers import DeleteCategoryHandler

    service = _get_delete_category_service(_get_category_repository(db), logger)
    return DeleteCategoryHandler(service, logger)


# ─────────────────────────────────────────────────────────────────
# QUERY HANDLERS (Read operations)
# ─────────────────────────────────────────────────────────────────


def find_category_by_id_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> FindCategoryByIdHandlerContract:
    """Factory for FindCategoryByIdHandler with all dependencies"""
    from app.context.category.application.handlers import FindCategoryByIdHandler

    service = _get_find_category_by_id_service(_get_category_repository(db), logger)
    return FindCategoryByIdHandler(service, logger)


def find_categories_by_user_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> FindCategoriesByUserHandlerContract:
    """Factory for FindCategoriesByUserHandler with all dependencies"""
    from app.context.category.application.handlers import FindCategoriesByUserHandler

    service = _get_find_categories_by_user_service(_get_category_repository(db), logger)
    return FindCategoriesByUserHandler(service, logger)


# ─────────────────────────────────────────────────────────────────
# PRIVATE HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────


def _get_category_repository(db: AsyncSession) -> CategoryRepositoryContract:
    """Private helper to get repository instance"""
    from app.context.category.infrastructure.repositories import CategoryRepository

    return CategoryRepository(db)


def _get_create_category_service(
    repository: CategoryRepositoryContract,
    logger: LoggerContract,
) -> CreateCategoryServiceContract:
    """Private helper to get create category service instance"""
    from app.context.category.domain.services import CreateCategoryService

    return CreateCategoryService(repository, logger)


def _get_update_category_service(
    repository: CategoryRepositoryContract,
    logger: LoggerContract,
) -> UpdateCategoryServiceContract:
    """Private helper to get update category service instance"""
    from app.context.category.domain.services import UpdateCategoryService

    return UpdateCategoryService(repository, logger)


def _get_delete_category_service(
    repository: CategoryRepositoryContract,
    logger: LoggerContract,
) -> DeleteCategoryServiceContract:
    """Private helper to get delete category service instance"""
    from app.context.category.domain.services import DeleteCategoryService

    return DeleteCategoryService(repository, logger)


def _get_find_category_by_id_service(
    repository: CategoryRepositoryContract,
    logger: LoggerContract,
) -> FindCategoryByIdServiceContract:
    """Private helper to get find category by ID service instance"""
    from app.context.category.domain.services import FindCategoryByIdService

    return FindCategoryByIdService(repository, logger)


def _get_find_categories_by_user_service(
    repository: CategoryRepositoryContract,
    logger: LoggerContract,
) -> FindCategoriesByUserServiceContract:
    """Private helper to get find categories by user service instance"""
    from app.context.category.domain.services import FindCategoriesByUserService

    return FindCategoriesByUserService(repository, logger)
