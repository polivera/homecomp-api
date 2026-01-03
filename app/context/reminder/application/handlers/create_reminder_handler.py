"""Handler for creating reminders"""

from app.context.reminder.application.commands import CreateReminderCommand
from app.context.reminder.application.contracts import CreateReminderHandlerContract
from app.context.reminder.application.dto import CreateReminderErrorCode, CreateReminderResult
from app.context.reminder.domain.contracts.services import CreateReminderServiceContract
from app.context.reminder.domain.exceptions import (
    InvalidReminderDateRangeError,
    InvalidReminderFrequencyError,
    ReminderMapperError,
)
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
from app.shared.domain.contracts import LoggerContract


class CreateReminderHandler(CreateReminderHandlerContract):
    """Handler for create reminder command"""

    def __init__(
        self,
        service: CreateReminderServiceContract,
        logger: LoggerContract,
    ):
        self._service = service
        self._logger = logger

    async def handle(self, command: CreateReminderCommand) -> CreateReminderResult:
        """Execute create reminder command"""

        try:
            # Convert primitives to value objects
            user_id = ReminderUserID(command.user_id)
            description = ReminderDescription(command.description)
            entry_type = ReminderEntryType(command.entry_type)
            currency = ReminderCurrency(command.currency)
            amount = ReminderOccurrenceAmount.from_float(command.amount)
            frequency = ReminderFrequency(command.frequency)
            start_date = ReminderStartDate(command.start_date)
            end_date = ReminderEndDate(command.end_date) if command.end_date else None
            category_id = ReminderCategoryID(command.category_id)

            # Call domain service
            reminder_dto = await self._service.create(
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

            # Validate result
            if reminder_dto.reminder_id is None:
                return CreateReminderResult(
                    error_code=CreateReminderErrorCode.UNEXPECTED_ERROR,
                    error_message="Failed to create reminder",
                )

            # Convert to result DTO
            return CreateReminderResult(
                reminder_id=reminder_dto.reminder_id.value,
                description=reminder_dto.description.value,
                entry_type=reminder_dto.entry_type.value,
                currency=reminder_dto.currency.value,
                frequency=reminder_dto.frequency.value,
                start_date=reminder_dto.start_date.value,
                end_date=reminder_dto.end_date.value if reminder_dto.end_date else None,
                category_id=reminder_dto.category_id.value if reminder_dto.category_id else None,
            )

        except InvalidReminderDateRangeError:
            return CreateReminderResult(
                error_code=CreateReminderErrorCode.INVALID_DATE_RANGE,
                error_message="End date cannot be before start date",
            )

        except InvalidReminderFrequencyError:
            return CreateReminderResult(
                error_code=CreateReminderErrorCode.INVALID_FREQUENCY,
                error_message="Invalid reminder frequency",
            )

        except ReminderMapperError:
            return CreateReminderResult(
                error_code=CreateReminderErrorCode.MAPPER_ERROR,
                error_message="Error mapping reminder data",
            )

        except Exception as e:
            self._logger.error(
                "Unexpected error creating reminder",
                user_id=command.user_id,
                entry_type=command.entry_type,
                start_date=command.start_date,
                error=str(e),
            )
            return CreateReminderResult(
                error_code=CreateReminderErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error creating reminder",
            )
