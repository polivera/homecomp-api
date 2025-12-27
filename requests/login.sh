#!/usr/bin/env bash

source ./base.sh

http --session=local_session POST "${MYAPP_URL}/api/auth/login" \
    email=user1@test.com \
    password=testonga
