#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./household_invite_user.sh <household_id> <invitee_user_id> <role>
# Example: ./household_invite_user.sh 1 2 participant

HOUSEHOLD_ID=${1:-1}
INVITEE_USER_ID=${2:-2}
ROLE=${3:-participant}

http --session=local_session POST "${MYAPP_URL}/api/households/${HOUSEHOLD_ID}/invites" \
    invitee_user_id:=${INVITEE_USER_ID} \
    role="${ROLE}"
