#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./household_remove_member.sh <household_id> <member_user_id>
# Example: ./household_remove_member.sh 1 2

HOUSEHOLD_ID=${1:-1}
MEMBER_USER_ID=${2:-2}

http --session=local_session DELETE "${MYAPP_URL}/api/households/${HOUSEHOLD_ID}/members/${MEMBER_USER_ID}"
