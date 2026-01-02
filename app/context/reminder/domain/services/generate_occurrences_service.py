"""Service for generating reminder occurrences"""

from datetime import datetime, timedelta

from app.context.reminder.domain.contracts.infrastructure import ReminderOccurrenceRepositoryContract
from app.context.reminder.domain.contracts.services import GenerateOccurrencesServiceContract
from app.context.reminder.domain.dto import ReminderOccurrenceDTO
from app.context.reminder.domain.exceptions import InvalidReminderFrequencyError
from app.context.reminder.domain.value_objects import (
    ReminderCategoryID,
    ReminderCurrency,
    ReminderDescription,
    ReminderEndDate,
    ReminderEntryType,
    ReminderFrequency,
    ReminderID,
    ReminderOccurrenceAmount,
    ReminderOccurrenceScheduledDate,
    ReminderOccurrenceStatus,
    ReminderStartDate,
)


class GenerateOccurrencesService(GenerateOccurrencesServiceContract):
    """Service for generating reminder occurrences based on frequency"""

    def __init__(self, occurrence_repo: ReminderOccurrenceRepositoryContract):
        self._occurrence_repo = occurrence_repo

    async def generate(
        self,
        reminder_id: ReminderID,
        frequency: ReminderFrequency,
        start_date: ReminderStartDate,
        end_date: ReminderEndDate | None,
        amount: ReminderOccurrenceAmount,
        description: ReminderDescription,
        entry_type: ReminderEntryType,
        currency: ReminderCurrency,
        category_id: ReminderCategoryID | None,
    ) -> list[ReminderOccurrenceDTO]:
        """Generate occurrences based on frequency and date range"""

        # Determine the end date for generation (1 year from start if no end_date)
        generation_end = end_date.value if end_date else self._add_years(start_date.value, 1)

        # Generate occurrence dates based on frequency
        occurrence_dates = self._generate_dates(frequency, start_date.value, generation_end)

        # Create occurrence DTOs
        occurrences: list[ReminderOccurrenceDTO] = []
        for scheduled_date in occurrence_dates:
            occurrence_dto = ReminderOccurrenceDTO(
                occurrence_id=None,  # Will be assigned by repository
                reminder_id=reminder_id,
                scheduled_date=ReminderOccurrenceScheduledDate.from_trusted_source(scheduled_date),
                amount=amount,
                status=ReminderOccurrenceStatus("pending"),
                entry_id=None,
            )
            occurrences.append(occurrence_dto)

        # Save all occurrences in batch
        if occurrences:
            await self._occurrence_repo.save_occurrences(occurrences)

        return occurrences

    def _generate_dates(self, frequency: ReminderFrequency, start: datetime, end: datetime) -> list[datetime]:
        """Generate list of occurrence dates based on frequency"""

        dates: list[datetime] = []
        current = start

        # Generate dates until we exceed the end date
        while current <= end:
            dates.append(current)
            current = self._next_occurrence(current, frequency)

        return dates

    def _next_occurrence(self, current: datetime, frequency: ReminderFrequency) -> datetime:
        """Calculate the next occurrence date based on frequency"""

        freq_value = frequency.value.lower()

        if freq_value == "daily":
            return current + timedelta(days=1)

        elif freq_value == "weekly":
            return current + timedelta(weeks=1)

        elif freq_value == "biweekly":
            return current + timedelta(weeks=2)

        elif freq_value == "monthly":
            return self._add_months(current, 1)

        elif freq_value == "quarterly":
            return self._add_months(current, 3)

        elif freq_value == "yearly":
            return self._add_years(current, 1)

        else:
            raise InvalidReminderFrequencyError(f"Unsupported frequency: {frequency.value}")

    def _add_months(self, dt: datetime, months: int) -> datetime:
        """
        Add months to a datetime, handling variable month lengths

        Examples:
        - Jan 31 + 1 month = Feb 28 (or 29 in leap year)
        - Jan 15 + 1 month = Feb 15
        - Dec 15 + 1 month = Jan 15 (next year)
        """
        # Calculate target month and year
        month = dt.month - 1 + months  # 0-indexed
        year = dt.year + month // 12
        month = month % 12 + 1  # Back to 1-indexed

        # Handle day overflow (e.g., Jan 31 -> Feb 28)
        day = min(dt.day, self._days_in_month(year, month))

        return dt.replace(year=year, month=month, day=day)

    def _add_years(self, dt: datetime, years: int) -> datetime:
        """
        Add years to a datetime, handling leap year Feb 29

        Examples:
        - Feb 29, 2024 + 1 year = Feb 28, 2025
        - Jan 15, 2024 + 1 year = Jan 15, 2025
        """
        target_year = dt.year + years

        # Handle Feb 29 in leap year -> non-leap year
        if dt.month == 2 and dt.day == 29 and not self._is_leap_year(target_year):
            return dt.replace(year=target_year, day=28)

        return dt.replace(year=target_year)

    def _days_in_month(self, year: int, month: int) -> int:
        """Return the number of days in a given month"""
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            return 29 if self._is_leap_year(year) else 28
        else:
            raise ValueError(f"Invalid month: {month}")

    def _is_leap_year(self, year: int) -> bool:
        """Check if a year is a leap year"""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
