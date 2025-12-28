"""Unit tests for FindCreditCardsByUserHandler"""

import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from app.context.credit_card.application.handlers.find_credit_cards_by_user_handler import (
    FindCreditCardsByUserHandler,
)
from app.context.credit_card.application.queries import FindCreditCardsByUserQuery
from app.context.credit_card.domain.dto import CreditCardDTO
from app.context.credit_card.domain.value_objects import (
    CardLimit,
    CardUsed,
    CreditCardAccountID,
    CreditCardCurrency,
    CreditCardID,
    CreditCardName,
    CreditCardUserID,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestFindCreditCardsByUserHandler:
    """Tests for FindCreditCardsByUserHandler"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_repository):
        """Create handler with mocked repository"""
        return FindCreditCardsByUserHandler(mock_repository)

    @pytest.fixture
    def sample_card_dtos(self):
        """Create sample card DTOs"""
        return [
            CreditCardDTO(
                credit_card_id=CreditCardID(1),
                user_id=CreditCardUserID(100),
                account_id=CreditCardAccountID(10),
                name=CreditCardName("Card 1"),
                currency=CreditCardCurrency("USD"),
                limit=CardLimit(Decimal("5000.00")),
                used=CardUsed(Decimal("1500.00")),
            ),
            CreditCardDTO(
                credit_card_id=CreditCardID(2),
                user_id=CreditCardUserID(100),
                account_id=CreditCardAccountID(10),
                name=CreditCardName("Card 2"),
                currency=CreditCardCurrency("EUR"),
                limit=CardLimit(Decimal("3000.00")),
                used=CardUsed(Decimal("500.00")),
            ),
        ]

    @pytest.mark.asyncio
    async def test_find_credit_cards_by_user_success(
        self, handler, mock_repository, sample_card_dtos
    ):
        """Test successful credit cards lookup"""
        # Arrange
        query = FindCreditCardsByUserQuery(user_id=100)

        mock_repository.find_user_credit_cards = AsyncMock(
            return_value=sample_card_dtos
        )

        # Act
        result = await handler.handle(query)

        # Assert
        assert len(result) == 2
        assert result[0].credit_card_id == 1
        assert result[0].name == "Card 1"
        assert result[1].credit_card_id == 2
        assert result[1].name == "Card 2"
        mock_repository.find_user_credit_cards.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_credit_cards_by_user_empty_list(self, handler, mock_repository):
        """Test user with no cards returns empty list"""
        # Arrange
        query = FindCreditCardsByUserQuery(user_id=100)

        mock_repository.find_user_credit_cards = AsyncMock(return_value=[])

        # Act
        result = await handler.handle(query)

        # Assert
        assert result == []
        mock_repository.find_user_credit_cards.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_credit_cards_by_user_none_returns_empty_list(
        self, handler, mock_repository
    ):
        """Test that None result returns empty list"""
        # Arrange
        query = FindCreditCardsByUserQuery(user_id=100)

        mock_repository.find_user_credit_cards = AsyncMock(return_value=None)

        # Act
        result = await handler.handle(query)

        # Assert
        assert result == []
        mock_repository.find_user_credit_cards.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_credit_cards_by_user_converts_primitives(
        self, handler, mock_repository, sample_card_dtos
    ):
        """Test that handler converts query primitives to value objects"""
        # Arrange
        query = FindCreditCardsByUserQuery(user_id=100)

        mock_repository.find_user_credit_cards = AsyncMock(
            return_value=sample_card_dtos
        )

        # Act
        await handler.handle(query)

        # Assert - verify repository was called with value objects
        call_args = mock_repository.find_user_credit_cards.call_args
        assert isinstance(call_args.kwargs["user_id"], CreditCardUserID)
        assert call_args.kwargs["user_id"].value == 100

    @pytest.mark.asyncio
    async def test_find_credit_cards_by_user_returns_application_dtos(
        self, handler, mock_repository, sample_card_dtos
    ):
        """Test that handler returns application layer DTOs (not domain DTOs)"""
        # Arrange
        query = FindCreditCardsByUserQuery(user_id=100)

        mock_repository.find_user_credit_cards = AsyncMock(
            return_value=sample_card_dtos
        )

        # Act
        result = await handler.handle(query)

        # Assert - verify results have primitive types (not value objects)
        for card in result:
            assert isinstance(card.credit_card_id, int)
            assert isinstance(card.user_id, int)
            assert isinstance(card.account_id, int)
            assert isinstance(card.name, str)
            assert isinstance(card.currency, str)
            assert isinstance(card.limit, Decimal)
            assert isinstance(card.used, Decimal)

    @pytest.mark.asyncio
    async def test_find_credit_cards_by_user_single_card(
        self, handler, mock_repository
    ):
        """Test finding single card for user"""
        # Arrange
        query = FindCreditCardsByUserQuery(user_id=100)

        single_card = [
            CreditCardDTO(
                credit_card_id=CreditCardID(1),
                user_id=CreditCardUserID(100),
                account_id=CreditCardAccountID(10),
                name=CreditCardName("Only Card"),
                currency=CreditCardCurrency("USD"),
                limit=CardLimit(Decimal("1000.00")),
                used=CardUsed(Decimal("0.00")),
            )
        ]

        mock_repository.find_user_credit_cards = AsyncMock(return_value=single_card)

        # Act
        result = await handler.handle(query)

        # Assert
        assert len(result) == 1
        assert result[0].name == "Only Card"
