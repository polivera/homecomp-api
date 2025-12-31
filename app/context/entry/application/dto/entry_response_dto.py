from dataclasses import dataclass

from app.context.entry.domain.dto import EntryDTO


@dataclass(frozen=True)
class EntryResponseDTO:
    """Application DTO for entry responses (primitives only)"""

    entry_id: int
    user_id: int
    account_id: int
    category_id: int
    entry_type: str
    entry_date: str  # ISO format
    amount: float
    description: str
    household_id: int | None = None

    @classmethod
    def from_domain_dto(cls, dto: EntryDTO) -> "EntryResponseDTO":
        """Convert domain DTO to application response DTO"""
        if dto.entry_id is None:
            raise ValueError("Entry ID cannot be None in response DTO")

        return cls(
            entry_id=dto.entry_id.value,
            user_id=dto.user_id.value,
            account_id=dto.account_id.value,
            category_id=dto.category_id.value,
            entry_type=dto.entry_type.value,
            entry_date=dto.entry_date.value.isoformat(),
            amount=float(dto.amount.value),
            description=dto.description.value,
            household_id=dto.household_id.value if dto.household_id else None,
        )
