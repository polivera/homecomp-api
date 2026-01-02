"""Handler for updating reminders"""

from app.context.reminder.application.commands import UpdateReminderCommand
from app.context.reminder.application.contracts import UpdateReminderHandlerContract
from app.context.reminder.application.dto import UpdateReminderErrorCode, UpdateReminderResult
from app.context.reminder.domain.contracts.services import UpdateReminderServiceContract
from app.context.reminder.domain.exceptions import (
    InvalidReminderDateRangeError,
    InvalidReminderFrequencyError,
    ReminderMapperError,
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


class UpdateReminderHandler(UpdateReminderHandlerContract):
    """Handler for update reminder command"""

    def __init__(self, service: UpdateReminderServiceContract):
        self._service = service

    async def handle(self, command: UpdateReminderCommand) -> UpdateReminderResult:
        """Execute update reminder command"""

        try:
            # Convert primitives to value objects
            reminder_id = ReminderID(command.reminder_id)
            user_id = ReminderUserID(command.user_id)
            description = ReminderDescription(command.description) if command.description else None
            entry_type = ReminderEntryType(command.entry_type) if command.entry_type else None
            currency = ReminderCurrency(command.currency) if command.currency else None
            frequency = ReminderFrequency(command.frequency) if command.frequency else None
            start_date = ReminderStartDate(command.start_date) if command.start_date else None
            end_date = ReminderEndDate(command.end_date) if command.end_date else None
            category_id = ReminderCategoryID(command.category_id) if command.category_id else None

            # Call domain service
            reminder_dto = await self._service.update(
                reminder_id=reminder_id,
                user_id=user_id,
                description=description,
                entry_type=entry_type,
                currency=currency,
                frequency=frequency,
                start_date=start_date,
                end_date=end_date,
                category_id=category_id,
            )

            # Convert to result DTO
            return UpdateReminderResult(
                reminder_id=reminder_dto.reminder_id.value if reminder_dto.reminder_id else None,
                description=reminder_dto.description.value,
                entry_type=reminder_dto.entry_type.value,
                currency=reminder_dto.currency.value,
                frequency=reminder_dto.frequency.value,
                start_date=reminder_dto.start_date.value,
                end_date=reminder_dto.end_date.value if reminder_dto.end_date else None,
                category_id=reminder_dto.category_id.value if reminder_dto.category_id else None,
            )

        except ReminderNotFoundError:
            return UpdateReminderResult(
                error_code=UpdateReminderErrorCode.REMINDER_NOT_FOUND,
                error_message="Reminder not found",
            )

        except ReminderNotBelongsToUserError:
            return UpdateReminderResult(
                error_code=UpdateReminderErrorCode.REMINDER_NOT_BELONGS_TO_USER,
                error_message="Reminder does not belong to user",
            )

        except InvalidReminderDateRangeError:
            return UpdateReminderResult(
                error_code=UpdateReminderErrorCode.INVALID_DATE_RANGE,
                error_message="End date cannot be before start date",
            )

        except InvalidReminderFrequencyError:
            return UpdateReminderResult(
                error_code=UpdateReminderErrorCode.INVALID_FREQUENCY,
                error_message="Invalid reminder frequency",
            )

        except ReminderMapperError:
            return UpdateReminderResult(
                error_code=UpdateReminderErrorCode.MAPPER_ERROR,
                error_message="Error mapping reminder data",
            )

        except Exception:
            return UpdateReminderResult(
                error_code=UpdateReminderErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error updating reminder",
            )
