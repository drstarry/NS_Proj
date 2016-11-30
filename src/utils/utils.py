#!/usr/bin/python2.7

from base64 import b64encode
import os


VERBOSE = True
SENT = True
RCVD = False


def vPrint(actor, sent, otherActor, toPrint, base64encode=True):
    """does verbose printing of stuff, with cutoffs for length and base 64
    encoding
    """
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
                toPrint = [b64encode(x) if len(x) < 100
                           else b64encode(x[:100]) + '...' for x in toPrint]
            else:
                toPrint = [x if len(x) < 100
                           else x[:100] + '...' for x in toPrint]
        print "%s: <%s>" % (label, toPrint)


def generateNonce(byteLength=32):
    """generates a large cryptographically secure byte string using
    `os.urandom`
    """
    return str(b64encode(os.urandom(byteLength)).decode('utf-8'))
