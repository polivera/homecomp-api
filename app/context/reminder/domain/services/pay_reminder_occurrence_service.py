"""Service for paying reminder occurrences"""

from app.context.reminder.domain.contracts.services import PayReminderOccurrenceServiceContract
from app.context.reminder.domain.value_objects import (
    ReminderOccurrenceAmount,
    ReminderOccurrenceID,
    ReminderPayAccountID,
    ReminderUserID,
)


class PayReminderOccurrenceService(PayReminderOccurrenceServiceContract):
    """Service that handles paying reminder occurrences"""

    def __init__(self):
        """
        Initialize the pay reminder occurrence service

        TODO: Add required dependencies (repositories, etc.) as parameters
        Example:
            def __init__(
                self,
                occurrence_repo: ReminderOccurrenceRepositoryContract,
                entry_repo: EntryRepositoryContract,  # Or similar
            ):
                self._occurrence_repo = occurrence_repo
                self._entry_repo = entry_repo
        """
        pass

    async def handle(
        self,
        occurrence_id: ReminderOccurrenceID,
        user_id: ReminderUserID,
        amount: ReminderOccurrenceAmount,
        account_id: ReminderPayAccountID,
    ) -> int:
        """
        Mark a reminder occurrence as paid and create corresponding entry

        TODO: Implement the payment logic:
        1. Fetch the occurrence by occurrence_id and user_id
        2. Verify occurrence exists, this also check if belongs to the user (raise OccurrenceNotFoundError if not)
        4. Check if already paid by checking if entry ID present (raise OccurrenceAlreadyPaidError if status is 'completed')
        5. Create an entry record (using entry repository/service) using the given amount and account_id
            Note: regarding entry update, we will modify entry context to also update account balance, don't do it here
        6. Update occurrence status to 'completed', set entry_id and update amount.
        7. Update future occurrence with the given amount
        8. Update associated reminder amount with the payed amount.
        9. Return the created entry_id

        Args:
            occurrence_id: The ID of the occurrence to pay
            user_id: The ID of the user paying the occurrence
            amount: The payed amount of the reminder for the specific occurrence
            account_id: What account has been used to generate the entry (actual payment)

        Returns:
            TBD, random int for now

        Raises:
            OccurrenceNotFoundError: If occurrence doesn't exist
            OccurrenceNotBelongsToUserError: If occurrence doesn't belong to user
            OccurrenceAlreadyPaidError: If occurrence is already paid
        """
        # TODO: Implement payment logic here
        raise NotImplementedError("Payment logic not yet implemented - fill this in!")
