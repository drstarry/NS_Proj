#!/usr/bin/python2.7

from socket import socket, AF_INET, SOCK_STREAM


class BaseClient:
    def Client(self, sckt, filename):
        """needs to be implemented by derived class
        must return:
        <boolean success>, <datetime time_taken>, <int attemps>
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

        success, time_taken, attempts = self.Client(serverSckt, bruteforce_file)
        # used to close socket when client is done
        serverSckt.sendCloseSignal()

        if success:
            print "Success! Cracked the password and got in."
        else:
            print "Failure! Tried to get in but couldn't."

        print "Took %d guesses and %d seconds." \
            % (attempts, time_taken.seconds)

        serverSckt.shutdown(1)  # send close signal to server socket
        serverSckt.close()  # close connection
