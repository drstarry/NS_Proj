#!/bin/sh

PORT=8000
PASSWORD_FILE='data/user_password_pairs.txt'
BRUTEFORCE_FILE='data/password_dictionary.txt'

if [[ $# -eq 1 ]]; then
  # optional argument
  PORT=$1
fi

# start server in the background
python src/main.py 'server' 'basic' $PORT $PASSWORD_FILE &
sleep 1
python src/main.py 'client' 'basic' $PORT $BRUTEFORCE_FILE
