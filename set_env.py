#!/usr/bin/python3

from os import environ

APP_PORT_DEFAULT = 7077

if port_ := environ.get('APP_PORT'):
    PORT = int(port_)
else:
    PORT = PORT_DEFAULT

#####=====----- THE END -----=====#########################################