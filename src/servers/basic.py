#!/usr/bin/python2.7

#from Crypto.PublicKey import RSA
#from Crypto.Hash import SHA
#from Crypto.Cipher import DES3
from socket import *
import utils


class Server:
  # sckt          = socket: the socket used to communicate
  # password_file = string: name of the file that contains username/password pairs
  def host(self, sckt, password_file):
    users = {}
    with open(password_file, "r") as f:
      for line in f.readlines():
        parts = line.strip().split(",")
        users.update({parts[0]: parts[1]}) # username, password

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


  # serverAddress = string: localhost/ip address/url
  # serverPort    = int:    port number to run server
  # password_file = string: name of the file that contains username/password pairs
  def start(self, serverAddress, serverPort, password_file):
    serverSckt = socket(AF_INET, SOCK_STREAM)    # get an IPv4 TCP socket object
    serverSckt.bind((serverAddress, serverPort)) # connect to host and port
    serverSckt.listen(1)                         # await requests
    print "Server: Listening at %s:%d" % (serverAddress, serverPort)
    sckt, addr = serverSckt.accept()             # accept a connection (blocking)

    self.host(sckt, password_file)

    sckt.shutdown(1)                             # send close signal
    sckt.close()                                 # close connection
