#!/usr/bin/python2.7

from datetime import datetime
from hashlib import sha1

from base import BaseClient
from utils import password
from utils import sockets


class HashedMetaClient(BaseClient):
    def Client(self, sckt, bruteforce_file):
        """
        sckt = socket: the socket used to communicate
        bruteforce_file = string: name of the file that has password guesses
        """
        success = False
        start_time = datetime.now()
        attempts = 0
        max_seconds_run = 5 * 60 # 5 minutes

        with open(bruteforce_file, "r") as f:
            for line in f.readlines():
                password_guess = line.strip()
                attempts = attempts + 1

                password_guess = sha1(password_guess).hexdigest()

                # [source ip address, username, password]
                guess_data = ["10.0.1.3", "sbarnesam", password_guess]
                sckt.sendData(guess_data)

                data = sckt.receiveRequest()
                if data == password.SUCCESS_AUTH:
                    success = True
                    break  # found a successful password!

                time_run = datetime.now() - start_time
                if time_run.seconds > max_seconds_run:
                    success = False
                    break  # timed out

        time_taken = datetime.now() - start_time
        return success, time_taken, attempts
