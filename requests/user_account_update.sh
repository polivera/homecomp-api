#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

http --session=local_session PUT "${MYAPP_URL}/api/user-accounts/accounts/2" \
    name="my-updated-account" \
    currency="ARS" \
    balance=423.55

    
