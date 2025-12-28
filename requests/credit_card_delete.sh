#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./credit_card_delete.sh <card_id>
# Example: ./credit_card_delete.sh 8

CARD_ID=${1:-1}

http --session=local_session DELETE "${MYAPP_URL}/api/credit-cards/cards/${CARD_ID}" 
