#!/usr/bin/env bash

source ./base.sh

 http --session=local_session POST "${MYAPP_URL}/api/user-accounts/accounts" \
     name="my third account" \
     balance=10554.34 \
     currency="ARS"
