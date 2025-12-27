#!/usr/bin/env bash

source ./base.sh

 http --session=local_session PUT "${MYAPP_URL}/api/user-accounts/accounts/2" \
     name="my-updated-account" \
     currency="ARS" \
     balance=423.55

    
