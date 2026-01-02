#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./user_account_create.sh <name> <balance> <currency>
# Example: ./user_account_create.sh "Savings Account" 1000.50 USD

NAME=${1:-"My Account"}
BALANCE=${2:-0}
CURRENCY=${3:-"USD"}

http --session=local_session POST "${MYAPP_URL}/api/user-accounts/accounts" \
    name="${NAME}" \
    balance="${BALANCE}" \
    currency="${CURRENCY}"
