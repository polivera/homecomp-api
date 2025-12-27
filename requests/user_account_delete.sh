#!/usr/bin/env bash

source ./base.sh

 http --session=local_session DELETE "${MYAPP_URL}/api/user-accounts/accounts/3"
