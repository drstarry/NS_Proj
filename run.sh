#!/bin/sh

PORT=8000
ACTOR_TYPE='basic'
SERVER_USER_DB='data/server_user_db.txt'
CLIENT_BRUTEFORCE_FILE='data/full_password_dictionary.txt'

if [[ $# -eq 1 ]]; then
  PORT=$1
elif [[ $# -eq 2 ]]; then
  PORT=$1
  ACTOR_TYPE=$2
fi

# start server in the background
python src/main.py 'server' $ACTOR_TYPE $PORT $SERVER_USER_DB &
sleep 1
python src/main.py 'client' $ACTOR_TYPE $PORT $CLIENT_BRUTEFORCE_FILE
