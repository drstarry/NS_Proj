#!/usr/bin/python2.7

from base64 import b64decode, b64encode
from types import MethodType
from socket import socket
import json


def sendData(self, msg):
    """sends a message over a socket
    """
    encodedList = []
    if type(msg) == str:
        encodedList = [b64encode(msg).decode('utf-8')]
    elif type(msg) == list:
        encodedList = [b64encode(piece).decode('utf-8') for piece in msg]
    serialized = json.dumps(encodedList)
    fullMsg = "%s\r\n\r\n" % serialized
    self.send(fullMsg)


def receiveRequest(self):
    """accepts requests until there has been a double newline. modified from:
    http://codereview.stackexchange.com/questions/15038/working-with-sockets
    """
    lines = []
    while True:
        line = readLine(self)
        if line == "\n" or line == "\r\n" or line == "":
            encodedResponse = json.loads("".join(lines).strip())
            if len(encodedResponse) == 1:
                return b64decode(encodedResponse[0].encode('utf-8'))
            else:
                return [b64decode(piece.encode('utf-8'))
                        for piece in encodedResponse]
        lines.append(line)


def readLine(sckt):
    """taken from:
    http://codereview.stackexchange.com/questions/15038/working-with-sockets
    """
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
