"""Handler for paying reminder occurrences"""

from app.context.reminder.application.commands import PayReminderOccurrenceCommand
from app.context.reminder.application.contracts import PayReminderOccurrenceHandlerContract
from app.context.reminder.application.dto import (
    PayReminderOccurrenceErrorCode,
    PayReminderOccurrenceResult,
)
from app.context.reminder.domain.contracts.services import PayReminderOccurrenceServiceContract
from app.context.reminder.domain.exceptions import (
    OccurrenceAlreadyPaidError,
    OccurrenceNotBelongsToUserError,
    OccurrenceNotFoundError,
)
from app.context.reminder.domain.value_objects import ReminderOccurrenceAmount, ReminderOccurrenceID, ReminderUserID
from app.context.reminder.domain.value_objects.reminder_pay_account_id import ReminderPayAccountID


class PayReminderOccurrenceHandler(PayReminderOccurrenceHandlerContract):
    """Handler for pay reminder occurrence command"""

    def __init__(self, service: PayReminderOccurrenceServiceContract):
        self._service = service

    async def handle(self, command: PayReminderOccurrenceCommand) -> PayReminderOccurrenceResult:
        """Execute pay reminder occurrence command"""

        try:
            # Convert primitives to value objects
            occurrence_id = ReminderOccurrenceID(command.occurrence_id)
            user_id = ReminderUserID(command.user_id)
            amount = ReminderOccurrenceAmount.from_float(command.amount)
            account_id = ReminderPayAccountID(command.account_id)

            # Call domain service
            entry_id = await self._service.handle(
                occurrence_id=occurrence_id, user_id=user_id, amount=amount, account_id=account_id
            )

            return PayReminderOccurrenceResult(paid=True, entry_id=entry_id)

        except OccurrenceNotFoundError:
            return PayReminderOccurrenceResult(
                error_code=PayReminderOccurrenceErrorCode.OCCURRENCE_NOT_FOUND,
                error_message="Occurrence not found",
            )

        except OccurrenceNotBelongsToUserError:
            return PayReminderOccurrenceResult(
                error_code=PayReminderOccurrenceErrorCode.OCCURRENCE_NOT_BELONGS_TO_USER,
                error_message="Occurrence does not belong to user",
            )

        except OccurrenceAlreadyPaidError:
            return PayReminderOccurrenceResult(
                error_code=PayReminderOccurrenceErrorCode.OCCURRENCE_ALREADY_PAID,
                error_message="Occurrence has already been paid",
            )

        except Exception:
            return PayReminderOccurrenceResult(
                error_code=PayReminderOccurrenceErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error paying occurrence",
            )
