#!/usr/bin/python2.7

from base import BaseServer
from utils import password
from utils import sockets


class ChallengeServer(BaseServer):
    def Host(self, sckt, password_file):
        """
        sckt = socket: the socket used to communicate
        password_file = string: file that contains username/password pairs
        """
        users = self.BuildDB(password_file)

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

            # adding extra step to require user to manually do something
            # human interaction is necessary here, which is why we're simply
            # sending back the wrong answer, because if the challenge is
            # correctly structured, a bot would never get this right
            challenge = "heyo"
            sckt.sendData(challenge)
            data = sckt.receiveRequest()
            if data == sockets.CLOSE_SIGNAL:
                # used to close socket when client is done
                break

            # check to make sure the data correctly works with the challenge
            if data != challenge:
                sckt.sendData(password.FAILURE_AUTH)
                continue

            if received_username in users and \
               users[received_username]["password"] == received_password:
                sckt.sendData(password.SUCCESS_AUTH)
            else:
                sckt.sendData(password.FAILURE_AUTH)
