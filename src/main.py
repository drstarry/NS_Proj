#!/usr/bin/python2.7

import time
import sys

from servers import basic as server_basic
from clients import basic as client_basic


# main "method" that kicks off various routines
if __name__ == "__main__":
    if not len(sys.argv) == 5:
        print "expected usage:\n\tpython main.py <'server'|'client'> \
              <actor type> <port> <data file>"
        exit(1)

    actor_str = sys.argv[1]
    actor_type = sys.argv[2]
    port = int(sys.argv[3])
    data_file_name = sys.argv[4]

    actor = None
    if actor_str == "server":
        if actor_type == "basic":
            actor = server_basic.Server()

    elif actor_str == "client":
        if actor_type == "basic":
            actor = client_basic.Client()

    if not actor:
        print "Bad arguments given"
        exit(1)

    actor.start("localhost", port, data_file_name)
