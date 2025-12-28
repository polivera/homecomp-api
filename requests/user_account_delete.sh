#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./user_account_delete.sh <account_id>
# Example: ./user_account_delete.sh 3

ACCOUNT_ID=${1:-1}

http --session=local_session DELETE "${MYAPP_URL}/api/user-accounts/accounts/${ACCOUNT_ID}"
