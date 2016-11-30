#!/usr/bin/python2.7

from socket import socket, AF_INET, SOCK_STREAM


class BaseClient:
    def Client(self, sckt, filename):
        """needs to be implemented by derived class
        """
        raise NotImplementedError

    def Start(self, serverAddress, serverPort, bruteforce_file):
        """
        serverHost = string: localhost/ip address/url for server
        serverPort = int: port number to connect for server
        bruteforce_file = string: name of the file that has password guesses
        """
        serverSckt = socket(AF_INET, SOCK_STREAM)
        serverSckt.connect((serverAddress, serverPort))
        print "Client: Connected to Server at %s:%d" \
            % (serverAddress, serverPort)

        self.Client(serverSckt, bruteforce_file)

        serverSckt.shutdown(1)  # send close signal to server socket
        serverSckt.close()  # close connection
