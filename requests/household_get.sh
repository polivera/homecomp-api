#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/base.sh"

# Usage: ./household_get.sh <household_id>
# Example: ./household_get.sh 1

HOUSEHOLD_ID=${1:-1}

http --session=local_session GET "${MYAPP_URL}/api/households/${HOUSEHOLD_ID}"
