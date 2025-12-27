#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

 http --session=local_session PUT "${MYAPP_URL}/api/credit-cards/cards/8" \
     account_id=2 \
     name="My booooo credit card" \
     currency="USD" \
     limit="2501"
