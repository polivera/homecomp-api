#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./credit_card_update.sh <card_id> <account_id> <name> <currency> <limit>
# Example: ./credit_card_update.sh 8 2 "Mastercard Premium" EUR 10000

CARD_ID=${1:-1}
ACCOUNT_ID=${2:-1}
NAME=${3:-"Updated Card"}
CURRENCY=${4:-"USD"}
LIMIT=${5:-1000}

http --session=local_session PUT "${MYAPP_URL}/api/credit-cards/cards/${CARD_ID}" \
    account_id:=${ACCOUNT_ID} \
    name="${NAME}" \
    currency="${CURRENCY}" \
    limit="${LIMIT}"
