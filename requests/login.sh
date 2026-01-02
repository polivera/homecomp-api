#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./login.sh <email> <password>
# Example: ./login.sh user1@test.com mypassword

EMAIL=${1:-"john.doe@example.com"}
PASSWORD=${2:-"testonga"}

http --session=local_session POST "${MYAPP_URL}/api/auth/login" \
    email="${EMAIL}" \
    password="${PASSWORD}"
