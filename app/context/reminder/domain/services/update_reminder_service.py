"""Service for updating reminders"""

from app.context.reminder.domain.contracts.infrastructure import (
    ReminderOccurrenceRepositoryContract,
    ReminderRepositoryContract,
)
from app.context.reminder.domain.contracts.services import (
    GenerateOccurrencesServiceContract,
    UpdateReminderServiceContract,
)
from app.context.reminder.domain.dto import ReminderDTO
from app.context.reminder.domain.exceptions import (
    InvalidReminderDateRangeError,
    ReminderNotBelongsToUserError,
    ReminderNotFoundError,
)
from app.context.reminder.domain.value_objects import (
    ReminderCategoryID,
    ReminderCurrency,
    ReminderDescription,
    ReminderEndDate,
    ReminderEntryType,
    ReminderFrequency,
    ReminderID,
    ReminderStartDate,
    ReminderUserID,
)


class UpdateReminderService(UpdateReminderServiceContract):
    """Service for updating reminders"""

    def __init__(
        self,
        reminder_repo: ReminderRepositoryContract,
        occurrence_repo: ReminderOccurrenceRepositoryContract,
        generate_occurrences_service: GenerateOccurrencesServiceContract,
    ):
        self._reminder_repo = reminder_repo
        self._occurrence_repo = occurrence_repo
        self._generate_occurrences_service = generate_occurrences_service

    async def update(
        self,
        reminder_id: ReminderID,
        user_id: ReminderUserID,
        description: ReminderDescription | None = None,
        entry_type: ReminderEntryType | None = None,
        currency: ReminderCurrency | None = None,
        frequency: ReminderFrequency | None = None,
        start_date: ReminderStartDate | None = None,
        end_date: ReminderEndDate | None = None,
        category_id: ReminderCategoryID | None = None,
    ) -> ReminderDTO:
        """Update an existing reminder and regenerate occurrences if needed"""

        # Fetch existing reminder with ownership check
        existing = await self._reminder_repo.find_user_reminder_by_id(reminder_id=reminder_id, user_id=user_id)

        if not existing:
            raise ReminderNotFoundError(f"Reminder {reminder_id.value} not found")

        if existing.user_id.value != user_id.value:
            raise ReminderNotBelongsToUserError(f"Reminder {reminder_id.value} does not belong to user")

        # Build updated reminder DTO (keep existing values if not provided)
        updated_reminder = ReminderDTO(
            reminder_id=reminder_id,
            user_id=user_id,
            description=description if description else existing.description,
            entry_type=entry_type if entry_type else existing.entry_type,
            currency=currency if currency else existing.currency,
            frequency=frequency if frequency else existing.frequency,
            start_date=start_date if start_date else existing.start_date,
            end_date=end_date if end_date is not None else existing.end_date,
            category_id=category_id if category_id is not None else existing.category_id,
        )

        # Validate date range
        if updated_reminder.end_date and updated_reminder.end_date.value < updated_reminder.start_date.value:
            raise InvalidReminderDateRangeError("End date cannot be before start date")

        # Check if frequency or dates changed (need to regenerate occurrences)
        needs_regeneration = frequency is not None or start_date is not None or end_date is not None

        # Update reminder
        saved_reminder = await self._reminder_repo.update_reminder(updated_reminder)

        # Regenerate occurrences if needed
        if needs_regeneration:
            # Delete old pending occurrences
            await self._occurrence_repo.delete_occurrences_by_reminder(reminder_id)

            # Generate new occurrences
            await self._generate_occurrences_service.generate(
                reminder_id=reminder_id,
                frequency=saved_reminder.frequency,
                start_date=saved_reminder.start_date,
                end_date=saved_reminder.end_date,
                description=saved_reminder.description,
                entry_type=saved_reminder.entry_type,
                currency=saved_reminder.currency,
                category_id=saved_reminder.category_id,
            )

        return saved_reminder
