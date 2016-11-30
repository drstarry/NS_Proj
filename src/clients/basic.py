#!/usr/bin/python2.7

from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM

from utils import sockets


class Client:
    def client(self, sckt, bruteforce_file):
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


    def start(self, serverAddress, serverPort, bruteforce_file):
        """
        serverHost = string: localhost/ip address/url for server
        serverPort = int: port number to connect for server
        bruteforce_file = string: name of the file that has password guesses
        """
        serverSckt = socket(AF_INET, SOCK_STREAM)
        serverSckt.connect((serverAddress, serverPort))
        print "Client: Connected to Server at %s:%d" \
            % (serverAddress, serverPort)

        self.client(serverSckt, bruteforce_file)

        serverSckt.shutdown(1)  # send close signal to server socket
        serverSckt.close()  # close connection
