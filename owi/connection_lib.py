# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 13:12:23 2018

@author: julouj
"""

import socket
import translator

LISTENING_PORT = 4224

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
        if self.socket_table=={}:
            return "no connections active"
        chain = "\n"
        for element in self.socket_table:
            chain += str(element) + "\n"
        return chain
    
            
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
            
            print("connected to " + str(name))
            
            return True
            
        except:
            print("couldn't connect to " + str(name))
            return False
        
        
    def end_connexion(self, name):
        """
        tries to end a connexion with the host at adress name in the hashtable
        can crash if unable to disconnect
        """
        
        self.socket_table[name].close()
        del self.socket_table[name]
        print("friendship ended with " + str(name))
        
        
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
            s.send(cocode(message))
            print("message sent")
            return True
        except:
            print("an error occured while sending message")
            return False
            
            
    def listen(self, name):
        """
        listen to the connexion referenced by name
        will pause the program until it receives a message 
        can crash if name isn't in the hashtable
        """
        
        s = self.socket_table[name]
        print("starting to listen " + str(name) + " indefinitely")
        try:
            data = s.recv(1024)
            print("data received")
            return decocode(data)
        except:
            print("an error occured during reception")
            try:
                self.end_connexion(name)
            except:
                return
            
            
    def listen_timed(self, name):
        """
        listen to the connexion referenced by name
        will pause the program until it receives a message 
        or if a timer of 10s expires (returning an empty string)
        can crash if name isn't in the hashtable
        """
        
        s = self.socket_table[name]
        print("starting to listen " + str(name) + " for 10s")
        try:
            s.settimeout(10)     #disallow listening in 10 seconds
            data = s.recv(1024)
            s.setblocking(True)  #reallow listening for that socket
            print("data received")
            return decocode(data)
        except:
            print("an error occured during reception")
            try:
                self.end_connexion(name)
            except:
                return
        
        
    def is_here(self,name):
        """
        returns whether name is present in the hashtable
        """
        return name in self.socket_table
        
    
    
    
    
    
    def send_nudes(self):
        """
        sends whoami to Johyn
        """
        addr = translator.Address()
        addr.create()
        
        payload = translator.Whoami()
        payload.create(1,addr,2,[translator.Var_str("node")])
        paie = payload.encode()
        l = len(paie)
        #print(list(ord(c) for c in paie))
        
        c = translator.Whoami()
        c.decode(paie)
        #print(c)
        
        #print(list(hex(ord(c)) for c in paie))
        
        a=translator.Message()
        a.create("whoami",l,paie)
        message = a.encode()
        
        print(list(hex(ord(c)) for c in message))
        #print(list(hex(c) for c in message.encode()))
        
        b=translator.Message()
        b.decode(message)
        print(b)
        
        c = translator.Whoami()
        #print(list((ord(c)) for c in str(b.payload)))
        c.decode(str(b.payload))
        print(c)
        
        #TCP_IP = "192.168.0.10"
        #TCP_IP = "78.248.188.120"
        TCP_IP = socket.gethostname()
        TCP_PORT = 4224
    
        name = "{}:{}".format(TCP_IP, TCP_PORT)    
    
        self.start_connexion(TCP_IP,TCP_PORT)
        self.send(name,message)
        print(self.listen_timed(name))
        #self.end_connexion(name)
        
        paie = ""
        l = 0
        a=translator.Message()
        a.create("whoamiack",l,paie)
        message = a.encode()
        self.send(name,message)
        print(self.listen(name))
        
def cocode(message):
    resulat = b''
    for elem in (c for c in message):
        n = ord(elem)
        resulat += n.to_bytes(1, 'big')
            
    return resulat

def decocode(message):
    resulat = ""
    for elem in (c for c in message):
        n=elem
        resulat += chr(n)
            
    return resulat
        
if __name__ == "__main__":
    C=Connexions()
    C.send_nudes()
