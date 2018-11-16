# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 12:58:18 2018

@author: Admin
"""

import socket
import json

class Connexions:
    """
    stores TCP connexions in a hashtable 
    and provides methods to ease communication 
    """
    
    def __init__(self):
        """
        creates the Connexions object
        """
        
        self.socket_table={}
    
    def __str__(self):
        """
        returns a list (in string) of couples (TCP_IP, TCP_PORT) 
        preceded by the adress in the hashtable
        """
        text = ""
        for key in self.socket_table:
            text += key
            text += "\n"
        return text
    
            
    def start_connexion(self, TCP_IP, TCP_PORT):
        """
        tries to establish a connexion with the host at TCP_IP on port TCP_PORT
        returns True if it is successful, False if it fails to connect
        the connexion is stored as TCP_IP:TCP_PORT
        """
        
        name = "{}:{}".format(TCP_IP, TCP_PORT)
        
        try:
            self.socket_table[name] = (socket.socket(socket.AF_INET, 
                                                     socket.SOCK_STREAM))
            self.socket_table[name].connect((TCP_IP, TCP_PORT))
            return True
            
        except:
            return False
        
    def end_connexion(self, name):
        """
        tries to end a connexion with the host at adress name in the hashtable
        can crash if unable to disconnect
        """
        
        self.socket_table[name].close()
        del self.socket_table[name]
        
    def obtain(self, name):
        """
        returns the socket linked to that name in the hashtable
        returns False if unable to find it
        """
        try:
            return self.socket_table[name]
            
        except:
            return False
            
    def send(self, name, message):
        """
        message has to be an unencoded string
        tries to send it to the host referenced by name in the hashtable
        returns True if it succeeds, False otherwise
        """
        try:
            s = self.socket_table[name]
            s.send(message.encode())
            return True
        except:
            return False
            
    def listen(self, name):
        """
        listen to the connexion referenced by name
        will pause the program until it receives a message 
        or if a timer of 10s expires (returning an empty string)
        can crash if name isn't in the hashtable
        """
        
        s = self.socket_table[name]
        try:
            s.settimeout(10)     #disallow listening in 10 seconds
            data = s.recv(1024)
            s.setblocking(True)  #reallow listening for that socket
            return data
        except:
            s.setblocking(True)  #reallow listening for that socket
            return ""
        
    def is_here(self,name):
        """
        returns whether name is present in the hashtable
        """
        return name in self.socket_table
        
    def send_nudes(self):
        """
        sends whoami to Johyn
        """
        
        f=open("whoami.json", "r")
    
        data = json.load(f)
        message = json.dumps(data)
        
        TCP_IP = socket.gethostname()
        #TCP_IP = '0.0.0.0'
        TCP_PORT = 4224
    
        name = "{}:{}".format(TCP_IP, TCP_PORT)    
    
        self.start_connexion(TCP_IP,TCP_PORT)
        self.send(name,message)
        print("message sent")
        print(self.listen(name))
        print("received")
        #self.end_connexion(name)
        
        f=open("whoaminvalide.json", "r")
        data = json.load(f)
        message = json.dumps(data)
        self.send(name,message)
        print(self.listen(name))
        #self.end_connexion(name)

C=Connexions()
C.send_nudes()
