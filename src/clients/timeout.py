#!/usr/bin/python2.7

from datetime import datetime

from base import BaseClient
from utils import password
from utils import sockets


class TimeoutClient(BaseClient):
    def Client(self, sckt, bruteforce_file):
        """
        sckt = socket: the socket used to communicate
        bruteforce_file = string: name of the file that has password guesses
        """
        success = False
        start_time = datetime.now()
        attempts = 0

        with open(bruteforce_file, "r") as f:
            for line in f.readlines():
                password_guess = line.strip()
                attempts = attempts + 1

                # [source ip address, username, password]
                # sfisherhi's password is #5 in the password dictionary file
                guess_data = ["10.0.1.3", "sfisherhi", password_guess]
                sckt.sendData(guess_data)
                data = sckt.receiveRequest()
                if data == password.SUCCESS_AUTH:
                    success = True
                    break  # found a successful password!

        time_taken = datetime.now() - start_time
        return success, time_taken, attempts
