# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 13:12:23 2018

@author: julouj
"""

import socket


import time
from connection_lib import *

LISTENING_PORT = 4224

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), LISTENING_PORT))
s.listen(3)

C=Connexions()

while True:
    (clientsocket, address) = s.accept()
    print(address)
    
    C.socket_table[address] = clientsocket

    message = C.listen(address)
    print(list(hex(ord(c)) for c in message))

    time.sleep(1)
    
    print(C)
    C.send(address,"ok")

