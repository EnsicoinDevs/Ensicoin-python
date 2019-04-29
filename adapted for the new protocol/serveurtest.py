# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 10:42:00 2018

@author: julouj
"""

import socket
import translator

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 4223))
s.listen(3)

while True:
    (clientsocket, address) = s.accept()
    print(address)
    a = clientsocket.recv(1024)
    
    b=translator.Message()
    b.decode(a.decode())
    print(b)
    
    message = "honk"
    clientsocket.send(message.encode())
    clientsocket.close()
