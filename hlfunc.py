# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 19:55:55 2018

@author: Admin
"""

import json
import socket
import threading
from fonctions_reponse import *
from commands import *

LISTENING_PORT = 4224


def msg_template():
    """
    returns the template of a message compatible with the protocol
    the dictionnary "message" is empty so it can be filled later
    """
    
    f=open("msg_template.json", "r")
    data = json.load(f)
    f.close()
    return data
    
    
def whoami():
    """
    returns a compatible whoami so it can be sent to another node
    """
    
    msg = msg_template()
    msg["message"]={"version":0}
    return msg
    
    
def init_control(C):
    """
    initializes a thread that listens to console inputs
    more details in the function 'control'
    """
    control_thread = threading.Thread(target=control, args=(C,))  
    control_thread.start()


def init_connections(C):
    """
    initializes C with the nodes whose addresses are stored in IPs.json
    it allows to automatically connect to known nodes
    """
    
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
        
        
def init_server():
    """
    returns a socket configured as a server
    """
    
    bind_ip = socket.gethostname()
    bind_port = LISTENING_PORT

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((bind_ip, bind_port))
    server.listen(3)
    return server
    
    
def wait_for_client(server,C):
    """
    stops the main thread until a client shows up
    when one does, the function 'connect' is called for him in a new thread
    """
    
    print("waiting for client")
    (client_socket, address) = server.accept()
    print('Connected to {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(target=connect, args=(client_socket,C,))  
    client_handler.start()
    

def connect(client_socket,C):
    """
    adds the client to the list of connections in C and sends him a whoami
    then, it loops until the connection is closed
    on connection ending, the thread will die in great suffering and with 
    many cries, but should not bother the other threads
    """
    
    request = client_socket.recv(1024).decode()
    print('Received ' + str(request))
    
    (TCP_IP,TCP_PORT) = client_socket.getpeername()
    name = "{}:{}".format(TCP_IP, TCP_PORT)
    
    C.socket_table[name]=client_socket
    C.send(name,whoami())
    
    while True:
        request = C.listen(name)
        
        print("message received from {}:".format(name))
        print(request)
        print()
        
        try:
            message = request["message"]
            m_type = request["type"]
        except:
            C.end_connexion(name)
            C.end_connexion(name)
            assert 1==0, "incorrect message: connection ended"
        
        process_message(message,m_type,name,C)


def process_message(message,m_type,name,C):
    """
    processes a received message
    the message has to be a dictionnary
    """
    if m_type in type_dict():
        type_dict()[m_type](message,name,C)
    else:
        C.send(name,"malpoli ! erreur: type inexistant")


def control(C):
    """
    structures the control thread
    loops undefinitely listening to console inputs
    commands are executed accordingly
    """
    while True:
        read=input()
        command = read.split()
        dico = command_dict()
        
        if command[0] in dico:
            dico[command[0]](command,C)
            
        else:
            print("unknown command, try using 'help'")















