# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 19:03:09 2018

@author: Admin
"""

import json
import socket
import threading
from connexionlib import *


#initialization----------------------------------------------------------
C=Connexions()

f=open("whoami.json", "r")
    
data = json.load(f)
message = json.dumps(data)
f.close()
        
ips=open("IPs.json", "r")
ip_data = json.load(ips)["iptable"]
ips.close()
        
for ip in ip_data:
    TCP_IP = ip[0]
    TCP_PORT = ip[1]
    
    name = "{}:{}".format(TCP_IP, TCP_PORT)    
    
    C.start_connexion(TCP_IP,TCP_PORT)
    C.send(name,message)
    print(C.listen(name))

#initialization----------------------------------------------------------

#server part--------------------------------------------------------------
bind_ip = '0.0.0.0'
bind_port = 4224

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(42)

def connect(client_socket):
    request = client_socket.recv(1024)
    print('Received ' + str(request))
    (TCP_IP,TCP_PORT) = client_socket.getpeername()
    name = "{}:{}".format(TCP_IP, TCP_PORT)
    C.socket_table[name]=client_socket
#server part--------------------------------------------------------------

#main loop------------------------------------------------------------------
while True:
    print(C)
    print("waiting for client")
    client_sock, address = server.accept()
    print('Connected to {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(target=connect, args=(client_sock,))  
    client_handler.start()
#main loop------------------------------------------------------------------
