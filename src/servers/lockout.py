#!/usr/bin/python2.7

import time

from base import BaseServer
from utils import password
from utils import sockets


class LockoutServer(BaseServer):
    def Host(self, sckt, password_file):
        """
        sckt = socket: the socket used to communicate
        password_file = string: file that contains username/password pairs
        """
        users = self.BuildDB(password_file)
        locked = []
        attempts = {}

        while True:
            # receive data from connected socket
            # data is in the format [source_ip, username, password]
            data = sckt.receiveRequest()
            if data == sockets.CLOSE_SIGNAL:
                # used to close socket when client is done
                break

            source_ip = data[0]
            received_username = data[1]
            received_password = data[2]

            # keep track of the number of attempts a user has made to log in
            # NOTE: in practice, this counter would need to get reset after
            # some amount of time
            # NOTE: the work-around to this prevention method is that the
            # attacker keeps the password fixed and tries logging in for many
            # different users. in this case we would probably want to try and
            # keep track of the source ip or something.
            if received_username in attempts:
                attempts[received_username] += 1
            else:
                attempts.update({received_username: 1})

            # user has 5 attempts to correctly log in
            # if account becomes locked after 5 attempts, user cannot get into
            # their account even with the correct username/password pair
            if attempts[received_username] > 5:
                locked.append(received_username)

            if received_username in users and \
               users[received_username]["password"] == received_password and \
               received_username not in locked:
                sckt.sendData(password.SUCCESS_AUTH)
            else:
                sckt.sendData(password.FAILURE_AUTH)
