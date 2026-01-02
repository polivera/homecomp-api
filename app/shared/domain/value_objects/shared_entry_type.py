from dataclasses import dataclass, field
from enum import Enum
from typing import Self


class SharedEntryTypeValues(str, Enum):
    """Entry type for financial entries"""

    INCOME = "income"
    EXPENSE = "expense"


@dataclass(frozen=True)
class SharedEntryType:
    """Entry type for financial entries"""

    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        """
        Create EntryType from string value.

        Args:
            value: String value ("income" or "expense")

        Returns:
            EntryType enum value

        Raises:
            ValueError: If value is not valid
        """
        if self.value != SharedEntryTypeValues.INCOME and self.value != SharedEntryTypeValues.EXPENSE:
            raise ValueError(f"Invalid entry type: '{self.value}'. Expected 'income' or 'expense'")

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        return cls(value, _validated=True)

    @classmethod
    def expense(cls) -> Self:
        return cls(SharedEntryTypeValues.EXPENSE)

    @classmethod
    def income(cls) -> Self:
        return cls(SharedEntryTypeValues.INCOME)
