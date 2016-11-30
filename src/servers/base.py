#!/usr/bin/python2.7

from socket import socket, AF_INET, SOCK_STREAM


class BaseServer:
    def Host(self, sckt, filename):
        """needs to be implemented by derived class
        """
        raise NotImplementedError

    def Start(self, serverAddress, serverPort, password_file):
        """
        serverAddress = string: localhost/ip address/url
        serverPort = int: port number to run server
        password_file = string: file that contains username/password pairs
        """
        serverSckt = socket(AF_INET, SOCK_STREAM)
        serverSckt.bind((serverAddress, serverPort))
        serverSckt.listen(1)  # await requests
        print "Server: Listening at %s:%d" % (serverAddress, serverPort)
        sckt, addr = serverSckt.accept()  # accept a connection (blocking)

        self.Host(sckt, password_file)

        sckt.shutdown(1)  # send close signal
        sckt.close()  # close connection
