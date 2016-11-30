#!/usr/bin/python2.7

from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM

from base import BaseClient
from utils import sockets


class BasicClient(BaseClient):
    def Client(self, sckt, bruteforce_file):
        """
        sckt = socket: the socket used to communicate
        bruteforce_file = string: name of the file that has password guesses
        """
        with open(bruteforce_file, "r") as f:
            password_guesses = [line.strip() for line in f.readlines()]

        success = False
        start_time = datetime.now()
        attempts = 0

        # TODO: need to find some way to find list of username/emails to guess
        for password_guess in password_guesses:
            attempts = attempts + 1

            # [source ip address, username, password]
            data = ["10.0.1.3", "example_username", password_guess]
            sckt.sendData(data)
            data = sckt.receiveRequest()
            if data == "SUCCESS":
                success = True
                break  # found a successful password!

        end_time = datetime.now()
        time_taken = end_time - start_time

        if success:
            print "Success! Cracked the password and got in."
        else:
            # used to close socket when client is done
            sckt.sendData("CLOSE")
            print "Failure! Tried to get in but couldn't."

        print "Took %d guesses and %d microseconds." \
            % (attempts, time_taken.microseconds)
