#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./user_account_update.sh <account_id> <name> <balance> <currency>
# Example: ./user_account_update.sh 2 "Updated Savings" 5000.00 EUR

ACCOUNT_ID=${1:-1}
NAME=${2:-"Updated Account"}
BALANCE=${3:-0}
CURRENCY=${4:-"USD"}

http --session=local_session PUT "${MYAPP_URL}/api/user-accounts/accounts/${ACCOUNT_ID}" \
    name="${NAME}" \
    balance="${BALANCE}" \
    currency="${CURRENCY}"
