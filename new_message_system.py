# -*- coding: utf-8 -*-
"""
Created on Wed Dec 4 13:16:04 2018

@author: julouj
"""
MAGIC = 422021



class uint32:
    
    def __init__(self,value):
        self.value = value
        
        
    def __str__(self):
        return str(self.value)
        
        
    def encode(self):
        pass
    
    
    def decode(self,code):
        pass
    


class uint64:
    
    def __init__(self,value):
        self.value = value
        
        
    def __str__(self):
        return str(self.value)
        
        
    def encode(self):
        pass
    
    
    def decode(self,code):
        pass



class var_uint:
    
    def __init__(self,value):
        self.value = value
        
        if 0 <= value <= 0xFF: 
            self.length = 8
            
        elif 0x100 <= value <= 0xFFFF:
            self.length = 16
            
        elif 0x10000 <= value <= 0xFFFFFFFF:
            self.length = 32
            
        elif 0x100000000 <= value <= 0xFFFFFFFFFFFFFFFF:
            self.length = 64
        
        
    def __str__(self):
        return str(self.value)
        
        
    def encode(self):
        pass
    
    
    def decode(self,code):
        pass



class message:
    
    def __init__(self, p_type="whoamiack", p_length=0, payload=None, magic=MAGIC):
        self.magic = magic
        self.type = p_type
        self.length = p_length
        self.payload = payload
        
        
    def __str__(self):
        output = "message:\n"
        output +="  type: " + str(self.type) + "\n"
        output +="  length: " + str(self.length) + "\n"
        return output
        
        
    def encode(self):
        pass
    
    
    def decode(self,code):
        pass
    
    
    
class address:
    
    def __init__(self, timestamp, ip, port):
        self.timestamp = timestamp
        self.ip = ip
        self.port = port
        
        
    def __str__(self):
        output = "address:\n"
        output +="  timestamp: " + str(self.timestamp) + "\n"
        output +="  ip: " + str(self.ip) + " port:" + str(self.port) + "\n"
        return output
        
        
    def encode(self):
        pass
    
    
    def decode(self,code):
        pass



class inv:
    
    def __init__(self, o_type, o_hash):
        self.type = o_type
        self.hash = o_type
        
        
    def __str__(self):
        output = "inv:\n"
        output +="  type: " + str(self.type) + "\n"
        output +="  hash: " + str(self.hash) + "\n"
        return output
        
        
    def encode(self):
        pass
    
    
    def decode(self,code):
        pass
    
    

class whoami:
    
    def __init__(self, version, timestamp):
        self.version = version
        self.timestamp = timestamp
        
        
    def __str__(self):
        output = "whoami:\n"
        output +="  version: " + str(self.version) + "\n"
        output +="  timestamp: " + str(self.timestamp) + "\n"
        return output
        
        
    def encode(self):
        pass
    
    
    def decode(self,code):
        pass



class addr:
    
    def __init__(self, count, addresses):
        self.count = count
        self.addresses = addresses
        
        
    def __str__(self):
        output = "whoami:\n"
        output +="  version: " + str(self.count) + "\n"
        output +="  timestamp: " + str(self.addresses) + "\n"
        return output
        
        
    def encode(self):
        pass
    
    
    def decode(self,code):
        pass


























