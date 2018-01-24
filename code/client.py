# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 15:26:28 2017

@author: Carter
@desc: Basic TCP client that sends a message and receives it back
"""

import socket 
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect socket to the port and host of the server
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    # Send data
    message = 'This is the msg. It will be repeated.'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)
    
    # Look for response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data
        
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

