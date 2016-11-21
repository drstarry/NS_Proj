#!/usr/bin/python2.7

from base64 import b64decode
from base64 import b64encode
from types import MethodType
from socket import *
import json
import sys
import os


VERBOSE = True


# does verbose printing of stuff, with cutoffs for length and base 64 encoding
SENT = True
RCVD = False
def vPrint(actor, sent, otherActor, toPrint, base64encode=True):
  if VERBOSE:
    label = "%s -> %s" % (actor, otherActor)
    if not sent:
      label = "%s <- %s" % (actor, otherActor)
    if len(label) < 12:
      label = label + (" " * (12 - len(label)))
    if type(toPrint) == str:
      if base64encode:
        toPrint = b64encode(toPrint)
      if len(toPrint) > 100:
        toPrint = toPrint[:100] + "..."
    elif type(toPrint) == list:
      if base64encode:
        toPrint = [b64encode(x) if len(x) < 100 else b64encode(x[:100]) + '...'
                   for x in toPrint]
      else:
        toPrint = [x if len(x) < 100 else x[:100] + '...' for x in toPrint]
    print "%s: <%s>" % (label, toPrint)



### SOCKET COMMUNICATION ###

# sends a message over a socket
def sendData(self, msg):
  encodedList = []
  if type(msg) == str:
    encodedList = [b64encode(msg).decode('utf-8')]
  elif type(msg) == list:
    encodedList = [b64encode(piece).decode('utf-8') for piece in msg]
  serialized = json.dumps(encodedList)
  fullMsg = "%s\r\n\r\n" % serialized
  self.send(fullMsg)

# accepts requests until there has been a double newline
# modified from:
# http://codereview.stackexchange.com/questions/15038/working-with-sockets
def receiveRequest(self):
  lines = []
  while True:
    line = readLine(self)
    if line == "\n" or line == "\r\n" or line == "":
      encodedResponse = json.loads("".join(lines).strip())
      if len(encodedResponse) == 1:
        return b64decode(encodedResponse[0].encode('utf-8'))
      else:
        return [b64decode(piece.encode('utf-8')) for piece in encodedResponse]
    lines.append(line)

# taken from:
# http://codereview.stackexchange.com/questions/15038/working-with-sockets
def readLine(sckt):
  chars = []
  while True:
    a = sckt.recv(1)
    chars.append(a)     
    if a == "\n" or a == "":
      return "".join(chars)

# can call socket.receiveRequest() and socket.sendData("x")
# make each of these custom functions available to the socket class
socket.receiveRequest = MethodType(receiveRequest, None, socket)
socket.sendData = MethodType(sendData, None, socket)



### RANDOM NUMBER GENERATION ###

# generates a large cryptographically secure byte string using `os.urandom`
def generateNonce(byteLength=32):
  return str(b64encode(os.urandom(byteLength)).decode('utf-8'))
