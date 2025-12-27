#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

 http --session=local_session POST "${MYAPP_URL}/api/credit-cards/cards" \
     account_id=1 \
     name="My pepino credit card" \
     currency="USD" \
     limit="4320"
