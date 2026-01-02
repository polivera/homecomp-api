#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./household_my_invites.sh
# Lists all pending household invitations for the authenticated user

http --session=local_session GET "${MYAPP_URL}/api/households/invites/pending"
