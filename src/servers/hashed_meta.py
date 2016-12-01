#!/usr/bin/python2.7

from hashlib import sha1

from base import BaseServer
from utils import password
from utils import sockets


class HashedMetaServer(BaseServer):
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

            if received_username not in users:
                sckt.sendData(password.FAILURE_AUTH)
                continue

            user = users[received_username]
            actual_password = user["password"]
            birthdate_keys = filter(lambda el: "birthdate" in el, user.keys())
            birthdate_meta_data = [user[k] for k in birthdate_keys]
            composed_password_data = actual_password + "," + \
                                     ",".join(birthdate_meta_data)
            actual_password = sha1(composed_password_data).hexdigest()

            if actual_password == received_password:
                sckt.sendData(password.SUCCESS_AUTH)
            else:
                sckt.sendData(password.FAILURE_AUTH)
