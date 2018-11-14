# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 19:03:09 2018

@author: Admin
"""

import json
import socket
import threading
from connexionlib import *
from gestionnaire_bloc import *
from fonctions_reponse import *

#initialization----------------------------------------------------------
C=Connexions()

f=open("whoami.json", "r")
data = json.load(f)
whoami = json.dumps(data)
f.close()
        
ips=open("IPs.json", "r")
ip_data = json.load(ips)["iptable"]
ips.close()

for ip in ip_data:
    TCP_IP = ip[0]
    TCP_PORT = ip[1]
    
    name = "{}:{}".format(TCP_IP, TCP_PORT)    
    
    C.start_connexion(TCP_IP,TCP_PORT)
    C.send(name,whoami)    #envoie un whoami 
    print(C.listen(name))

#initialization----------------------------------------------------------

#server part--------------------------------------------------------------
bind_ip = socket.gethostname()
bind_port = 4224

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
server.listen(3)


def connect(client_socket):
    request = client_socket.recv(1024)
    print('Received ' + str(request))
    (TCP_IP,TCP_PORT) = client_socket.getpeername()
    name = "{}:{}".format(TCP_IP, TCP_PORT)
    C.socket_table[name]=client_socket
    C.send(name,whoami)
    print(C)
    while True:
        request = client_socket.recv(1024)
        print("message received from {}:".format(name))
        print(request)
        message = request["message"]
        
        if "version" in message: #whoami
            C.send(name,whoami)
            
        elif "types" in message: #inv et notfound
        
            if message["types"] is not None:
                C.send(name,ans_inv(message))
            else:
                C.send(name,ans_notfound(message))
                
        elif "inv" in message: #getdata
            C.send(name,ans_getdata(message))
        
    
#server part--------------------------------------------------------------

#main loop------------------------------------------------------------------

while True:
    print("waiting for client")
    (client_socket, address) = server.accept()
    print('Connected to {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(target=connect, args=(client_socket,))  
    client_handler.start()
    
#main loop------------------------------------------------------------------


































