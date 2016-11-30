#!/usr/bin/python2.7

import sys

from servers.basic import BasicServer
from clients.basic import BasicClient
from servers.hashed_meta import HashedMetaServer
from clients.hashed_meta import HashedMetaClient


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
            print "Basic Server",
            actor = BasicServer()
        if actor_type == "hashed_meta":
            print "Hashed Meta Server",
            actor = HashedMetaServer()

    elif actor_str == "client":
        if actor_type == "basic":
            print "Basic Client",
            actor = BasicClient()
        if actor_type == "hashed_meta":
            print "Hashed Meta Client",
            actor = HashedMetaClient()

    if not actor:
        print "Bad arguments given"
        exit(1)

    actor.Start("localhost", port, data_file_name)
