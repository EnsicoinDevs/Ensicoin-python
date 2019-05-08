# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 19:34:19 2018

@author: Admin
"""

from connexionlib import *
from hlfunc import *

C = Connexions()

def main():
    init_control(C) #creates the control thread
    print("control set up")
    init_connections(C) #read ips from json and connects them in C
    print("connexion storage initiated")
    server = init_server() #creates a socket configured for the server
    print("server configured")    
    
    while True:
        wait_for_client(server,C) #waits until a client connects to server
                                  #and creates a thread to deal with him
main()