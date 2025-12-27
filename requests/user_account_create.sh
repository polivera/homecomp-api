#!/usr/bin/env bash

source ./base.sh

 http --session=local_session POST "${MYAPP_URL}/api/user-accounts/accounts" \
     name="my pindonga account" \
     balance=554.34 \
     currency="USD"
