#!/usr/bin/python3
#
# This is a very simple SERVER implementation for a very very simple
# request/reply protocol.
#
import socket
import sys

if len(sys.argv) > 1:
    port_number = int(sys.argv[1])
else:
    port_number = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', port_number))
s.listen(1)

def answer(conn, addr):
    print('Serving a connection from host', addr[0], 'on port', addr[1])
    request = conn.recv(1024)   # reading data (a request) from the connection
    print('request:', request.decode('utf-8'))
    reply = input('reply> ')
    conn.send(reply.encode('utf-8'))
    conn.close()


while True:
    print('Accepting connections')
    conn, addr = s.accept()
    thread_create(answer(conn, addr))

s.close()