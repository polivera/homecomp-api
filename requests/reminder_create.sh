#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./reminder_create.sh <description> <amount> <entry_type> <currency> <frequency> <start_date> [category_id] [end_date]
# Example: ./reminder_create.sh "Monthly Rent" 1500.00 "expense" "USD" "monthly" "2026-01-15T00:00:00Z"
# Example with end date: ./reminder_create.sh "Gym Membership" 50.00 "expense" "USD" "monthly" "2026-01-01T00:00:00Z" 1 "2026-12-31T23:59:59Z"
# Example with category: ./reminder_create.sh "Salary" 5000.00 "income" "USD" "monthly" "2026-01-01T00:00:00Z" 1

DESCRIPTION=${1:-"Monthly Reminder"}
AMOUNT=${2:-100.00}
ENTRY_TYPE=${3:-"expense"}
CURRENCY=${4:-"USD"}
FREQUENCY=${5:-"monthly"}
START_DATE=${6:-"2026-01-15T00:00:00Z"}
CATEGORY_ID=${7:-1}
END_DATE=${8:-""}

# Build the request
REQUEST_ARGS=(
    "${MYAPP_URL}/api/reminders"
    description="${DESCRIPTION}"
    amount="${AMOUNT}"
    entry_type="${ENTRY_TYPE}"
    currency="${CURRENCY}"
    frequency="${FREQUENCY}"
    start_date="${START_DATE}"
)

# Add optional end_date if provided
if [ -n "${END_DATE}" ]; then
    REQUEST_ARGS+=(end_date="${END_DATE}")
fi

# Add optional category_id if provided
if [ -n "${CATEGORY_ID}" ]; then
    REQUEST_ARGS+=(category_id:="${CATEGORY_ID}")
fi

http --session=local_session POST "${REQUEST_ARGS[@]}"
