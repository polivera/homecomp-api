#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./household_update.sh <household_id> <name>
# Example: ./household_update.sh 1 "Updated Household Name"

HOUSEHOLD_ID=${1:-1}
NAME=${2:-"Updated Household"}

http --session=local_session PUT "${MYAPP_URL}/api/households/${HOUSEHOLD_ID}" \
    name="${NAME}"
