from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UpdateCreditCardResult:
    """Result of credit card update operation"""

    success: bool = False
    error: Optional[str] = None
