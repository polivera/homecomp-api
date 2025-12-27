from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateCreditCardResponse:
    success: bool
    message: str
