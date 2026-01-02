#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./credit_card_create.sh <account_id> <name> <currency> <limit>
# Example: ./credit_card_create.sh 1 "Visa Gold" USD 5000

ACCOUNT_ID=${1:-1}
NAME=${2:-"My Credit Card"}
CURRENCY=${3:-"USD"}
LIMIT=${4:-1000}

http --session=local_session POST "${MYAPP_URL}/api/credit-cards/cards" \
    account_id:=${ACCOUNT_ID} \
    name="${NAME}" \
    currency="${CURRENCY}" \
    limit="${LIMIT}"
