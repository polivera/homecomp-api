#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./household_decline_invite.sh <household_id>
# Example: ./household_decline_invite.sh 1

HOUSEHOLD_ID=${1:-1}

http --session=local_session POST "${MYAPP_URL}/api/households/${HOUSEHOLD_ID}/invites/decline"
