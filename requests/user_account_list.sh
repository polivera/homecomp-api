#!/usr/bin/env bash

source ./base.sh

 http --session=local_session GET "${MYAPP_URL}/api/user-accounts/accounts"
