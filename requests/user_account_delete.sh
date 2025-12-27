#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

 http --session=local_session DELETE "${MYAPP_URL}/api/user-accounts/accounts/3"
