#!/usr/bin/env bash

source ./base.sh

http --session=local_session DELETE "${MYAPP_URL}/api/credit-cards/cards/8" 
