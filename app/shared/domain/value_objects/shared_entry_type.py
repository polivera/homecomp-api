from dataclasses import dataclass
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

    @classmethod
    def from_string(cls, str_value: str) -> Self:
        """
        Create EntryType from string value.

        Args:
            value: String value ("income" or "expense")

        Returns:
            EntryType enum value

        Raises:
            ValueError: If value is not valid
        """
        if str_value != SharedEntryTypeValues.INCOME and str_value != SharedEntryTypeValues.EXPENSE:
            raise ValueError(f"Invalid entry type: '{str_value}'. Expected 'income' or 'expense'")

        return cls(value=str_value)

    @classmethod
    def expense(cls) -> Self:
        return cls(SharedEntryTypeValues.EXPENSE)

    @classmethod
    def income(cls) -> Self:
        return cls(SharedEntryTypeValues.INCOME)
