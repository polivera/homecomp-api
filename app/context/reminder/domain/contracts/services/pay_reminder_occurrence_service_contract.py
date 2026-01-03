"""Contract for pay reminder occurrence service"""

from abc import ABC, abstractmethod

from app.context.reminder.domain.value_objects import ReminderOccurrenceAmount, ReminderOccurrenceID, ReminderUserID
from app.context.reminder.domain.value_objects.reminder_pay_account_id import ReminderPayAccountID


class PayReminderOccurrenceServiceContract(ABC):
    """Contract for service that handles paying reminder occurrences"""

    @abstractmethod
    async def handle(
        self,
        occurrence_id: ReminderOccurrenceID,
        user_id: ReminderUserID,
        amount: ReminderOccurrenceAmount,
        account_id: ReminderPayAccountID,
    ) -> int:
        """
        Mark a reminder occurrence as paid and create corresponding entry

        Args:
            occurrence_id: The ID of the occurrence to pay
            user_id: The ID of the user paying the occurrence

        Returns:
            The entry_id created for this payment

        Raises:
            OccurrenceNotFoundError: If occurrence doesn't exist
            OccurrenceNotBelongsToUserError: If occurrence doesn't belong to user
            OccurrenceAlreadyPaidError: If occurrence is already paid
        """
        pass
