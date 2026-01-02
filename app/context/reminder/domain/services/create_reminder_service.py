"""Service for creating reminders"""

from app.context.reminder.domain.contracts.infrastructure import ReminderRepositoryContract
from app.context.reminder.domain.contracts.services import (
    CreateReminderServiceContract,
    GenerateOccurrencesServiceContract,
)
from app.context.reminder.domain.dto import ReminderDTO
from app.context.reminder.domain.exceptions import InvalidReminderDateRangeError
from app.context.reminder.domain.value_objects import (
    ReminderCategoryID,
    ReminderCurrency,
    ReminderDescription,
    ReminderEndDate,
    ReminderEntryType,
    ReminderFrequency,
    ReminderOccurrenceAmount,
    ReminderStartDate,
    ReminderUserID,
)


class CreateReminderService(CreateReminderServiceContract):
    """Service for creating reminders and generating occurrences"""

    def __init__(
        self,
        reminder_repo: ReminderRepositoryContract,
        generate_occurrences_service: GenerateOccurrencesServiceContract,
    ):
        self._reminder_repo = reminder_repo
        self._generate_occurrences_service = generate_occurrences_service

    async def create(
        self,
        user_id: ReminderUserID,
        amount: ReminderOccurrenceAmount,
        description: ReminderDescription,
        entry_type: ReminderEntryType,
        currency: ReminderCurrency,
        frequency: ReminderFrequency,
        start_date: ReminderStartDate,
        category_id: ReminderCategoryID,
        end_date: ReminderEndDate | None = None,
    ) -> ReminderDTO:
        """Create a new reminder and generate initial occurrences"""

        # Validate date range
        if end_date and end_date.value < start_date.value:
            raise InvalidReminderDateRangeError("End date cannot be before start date")

        # Create reminder DTO
        reminder_dto = ReminderDTO(
            reminder_id=None,  # Will be assigned by repository
            user_id=user_id,
            description=description,
            entry_type=entry_type,
            currency=currency,
            amount=amount,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
            category_id=category_id,
        )

        # Save reminder
        saved_reminder = await self._reminder_repo.save_reminder(reminder_dto)

        # Generate occurrences
        if saved_reminder.reminder_id:
            await self._generate_occurrences_service.generate(
                reminder_id=saved_reminder.reminder_id,
                frequency=frequency,
                start_date=start_date,
                end_date=end_date,
                amount=amount,
                description=description,
                entry_type=entry_type,
                currency=currency,
                category_id=category_id,
            )

        return saved_reminder
