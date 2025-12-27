#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

http --session=local_session POST "${MYAPP_URL}/api/households/" \
    name="My Household" 
