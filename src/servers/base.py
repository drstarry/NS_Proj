#!/usr/bin/python2.7

from socket import socket, AF_INET, SOCK_STREAM


class BaseServer:
    def Host(self, sckt, filename):
        """needs to be implemented by derived class
        """
        raise NotImplementedError


    def BuildDB(self, filename):
        """builds a dict of user information parsed from a file
        """
        format_key = "FORMAT:"
        line_format = []
        users = {}

        with open(filename, "r") as f:
            for line in f.readlines():
                line = line.strip()

                if len(line) == 0:
                    # skip empty lines
                    continue

                if line[:2] == "##" and format_key in line:
                    # lines starting with '##' and have "FORMAT" are for formatting
                   line = line[line.find(format_key) + len(format_key):].strip()
                   line_format = map(lambda part: part.strip(), line.split(","))
                   continue

                if line[0] == "#":
                    # skip lines starting with "#" - comments
                    continue

                if len(line_format) == 0:
                    # if no formatting line has been found before any real data,
                    # throw an error
                    print "You must specify a format line at the top of your",
                    print "user db file! expects the format:"
                    print "# FORMAT: username, password, thing1, thing2"
                    raise AttributeError
                    break

                if not ("username" in line_format and "password" in line_format):
                    # if both "username" and "password" are not provided in the
                    # formatting lines, throw an error. these are required
                    print "You must provide a username and password for each",
                    print "user\n# FORMAT: username, password, thing1, thing2"
                    raise AttributeError
                    break

                parts = line.split(",")
                user_info = {}
                for idx, key in enumerate(line_format):
                   if len(parts) > idx:
                       user_info.update({key: parts[idx].strip()})
                   else:
                       user_info.update({key: ""})
                username = user_info["username"]

                users.update({username: user_info})

        return users


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
