#!/usr/bin/python2.7

from socket import socket, AF_INET, SOCK_STREAM

from base import BaseServer
from utils import sockets


class BasicServer(BaseServer):
    def Host(self, sckt, password_file):
        """
        sckt = socket: the socket used to communicate
        password_file = string: file that contains username/password pairs
        """
        users = {}
        with open(password_file, "r") as f:
            for line in f.readlines():
                parts = line.strip().split(",")
                users.update({parts[0]: parts[1]})  # username, password

        while True:
            # receive data from connected socket
            # data is in the format [source_ip, username, password]
            data = sckt.receiveRequest()
            if data == "CLOSE":
                # used to close socket when client is done
                break

            source_ip = data[0]
            username = data[1]
            password = data[2]

            if username in users and users[username] == password:
                sckt.sendData("SUCCESS!")
                break
            else:
                sckt.sendData("FAILURE!")
