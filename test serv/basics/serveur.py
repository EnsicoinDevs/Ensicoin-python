# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 19:31:40 2018

@author: Admin
"""

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 4224))
s.listen(3)

while True:
    (clientsocket, address) = s.accept()
    print(address)