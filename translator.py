# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 12:48:04 2018
@author: julouj
"""

MAGIC = 422021


def iter_bytes(n):
    hexa = hex(n)[2:]
    if len(hexa)%2 == 1:
        hexa = "0"+hexa
    while hexa != "":
        yield int(("0x" + hexa[0:2]),16)
        hexa = hexa[2:]
        
        
def encode_number(n,longueur):
    witch = ""
    for byte in iter_bytes(n):
        witch += chr(byte)
    return chr(0x00)*(int(longueur)-len(witch)) + witch
    
    
def decode_number(encoded_n):
    i=len(encoded_n)-1
    n=0
    for c in encoded_n:
        k = ord(c)
        n += (256**i)*k
        i-=1
    return n


def encode_string(s,longueur):
    return s + chr(0x00)*(int(longueur)-len(s))


def decode_string(encoded_s):
    s = ""
    for c in encoded_s:
        if c != chr(0):
            s+=c
    return s

    
    
def decode_message(code):
    magic = code[0:4]
    m_type = code[4:16]
    m_length = code[16:24]
    payload = code[24:]
    
    return (decode_number(magic),
            decode_string(m_type),
            decode_number(m_length),
            decode_string(payload))
            
            
def decode_address(code):
    timestamp = code[0:8]
    ip = code[8:24]
    port = code[24:26]
    
    return (decode_number(timestamp),
            decode_string(ip),
            decode_number(port))
    
    
class Uint16:
    
    def __init__(self, value):
        self.value = int(value)
        
    def __str__(self):
        return str(self.value)
        
    def encode(self):
        return encode_number(self.value,2)
        
    def __int__(self):
        return self.value
        
        

class Uint32:
    
    def __init__(self, value):
        self.value = int(value)
        
    def __str__(self):
        return str(self.value)
        
    def encode(self):
        return encode_number(self.value,4)

    def __int__(self):
        return self.value
        
        

class Uint64:
    
    def __init__(self, value):
        self.value = int(value)
        
    def __str__(self):
        return str(self.value)
        
    def encode(self):
        return encode_number(self.value,8)
        
    def __int__(self):
        return self.value
    


class Var_uint:
    
    def __init__(self, value):
        self.value = int(value)
        
        if 0 <= int(value) <= 0xFF: 
            self.length = 8
            
        elif 0x100 <= int(value) <= 0xFFFF:
            self.length = 16
            
        elif 0x10000 <= int(value) <= 0xFFFFFFFF:
            self.length = 32
            
        elif 0x100000000 <= int(value) <= 0xFFFFFFFFFFFFFFFF:
            self.length = 64
        
        
    def __str__(self):
        return str(self.value)
        
        
    def encode(self):
        dico = {8:"", 16:"FD", 32:"FE", 64:"FF"}
        return dico[self.length] + encode_number(self.value,self.length//4)
        
    def __int__(self):
        return self.value
        
        

class Finite_string:
    
    def __init__(self, value, length):
        self.value = str(value)
        self.length = Var_uint(length)
        
    def __str__(self):
        return str(self.value)
        
    def encode(self):
        return encode_string(self.value, self.length)
        
        
        
class Var_array():
    def __init__(self, values, length):
        
        self.values = ""
        for value in values:
            self.values += str(value)
            
        self.length = Var_uint(length)
        
    def __str__(self):
        return str(self.values)
        
    def encode(self):
        return self.length.encode() + self.values
    


class Message:
    
    def __init__(self, p_type="whoamiack", p_length=0, payload="", magic=MAGIC):
        self.magic = Uint32(magic)
        self.type = Finite_string(p_type, 12)
        self.length = Uint64(p_length)
        self.payload = Finite_string(payload, self.length)
        
        
    def __str__(self):
        output = "message:\n"
        output +="  type: " + str(self.type) + "\n"
        output +="  length: " + str(self.length) + "\n"
        return output
        
        
    def encode(self):
        return self.magic.encode() + self.type.encode() + self.length.encode() + self.payload.encode()
    
    
    
class Address:
    
    def __init__(self, timestamp, ip, port):
        self.timestamp = Uint64(timestamp)
        self.ip = Finite_string(ip, 16)
        self.port = Uint16(port)
        
        
    def __str__(self):
        output = "address:\n"
        output +="  timestamp: " + str(self.timestamp) + "\n"
        output +="  ip: " + str(self.ip) + " port:" + str(self.port) + "\n"
        return output
        
        
    def encode(self):
        return self.timestamp.encode() + self.ip.encode() + self.port.encode()



class Inv_vect:
    
    def __init__(self, o_type, o_hash):
        self.type = Uint32(o_type)
        self.hash = Finite_string(o_hash,32)
        
        
    def __str__(self):
        output = "inv_vect:\n"
        output +="  type: " + str(self.type) + "\n"
        output +="  hash: " + str(self.hash) + "\n"
        return output
        
        
    def encode(self):
        return self.type.encode() + self.hash.encode()
    
    

class Whoami:
    
    def __init__(self, version, timestamp):
        self.version = Uint32(version)
        self.timestamp = Uint64(timestamp)
        
        
    def __str__(self):
        output = "whoami:\n"
        output +="  version: " + str(self.version) + "\n"
        output +="  timestamp: " + str(self.timestamp) + "\n"
        return output
        
        
    def encode(self):
        return self.version.encode() + self.timestamp.encode()



class Addr:
    
    def __init__(self, count, addresses):
        self.count = Var_uint(count)
        self.addresses = Var_array(addresses)
        
        
    def __str__(self):
        output = "addr:\n"
        output +="  count: " + str(self.count) + "\n"
        output +="  addresses: " + str(self.addresses) + "\n"
        return output
        
        
    def encode(self):
        return self.count.encode() + self.addresses.encode()
    
    
class Inv:
    
    def __init__(self, count, inventory):
        self.count = Var_uint(count)
        self.inventory = Var_array(inventory)
        
        
    def __str__(self):
        output = "inv:\n"
        output +="  count: " + str(self.count) + "\n"
        output +="  inventory: " + str(self.inventory) + "\n"
        return output
        
        
    def encode(self):
        return self.count.encode() + self.inventory.encode()
    
    

class Block:
    
    def __init__(self, version, flags_count, flags, prev_block, merkle_root,
                 timestamp, height, bits, nonce, transactions_count, 
                 transactions):
                     
        self.version = Uint32(version)
        self.flags_count = Var_uint(flags_count)
        self.flags = Var_array(flags)
        self.prev_block = Finite_string(prev_block, 32)
        self.merkle_root = Finite_string(merkle_root, 32)
        self.timestamp = Uint64(timestamp)
        self.height = Uint32(height)
        self.bits = Uint32(bits)
        self.nonce = Uint64(nonce)
        self.transactions_count = Var_uint(transactions_count)
        self.transactions = Var_array(transactions)
        
        
    def __str__(self):
        output = "block:\n"
        output +="  version: " + str(self.version) + "\n"
        output +="  prev_block: " + str(self.prev_block) + "\n"
        output +="  height: " + str(self.height) + "\n"
        return output
        
        
    def encode(self):
        
        debut = self.version.encode() + self.flags_count.encode() + self.flags.encode()
        milieu1 = self.prev_block.encode() + self.merkle_root.encode() + self.timestamp.encode()
        milieu2 = self.height.encode() + self.bits.encode() + self.nonce.encode()
        fin = self.transactions_count.encode() + self.transactions.encode()
        
        return debut + milieu1 + milieu2 + fin
        
        
        
class Transaction:
    
    def __init__(self, version, flags_count, flags, inputs_count, inputs, outputs_count, outputs):
                     
        self.version = Uint32(version)
        self.flags_count = Var_uint(flags_count)
        self.flags = Var_array(flags)
        self.inputs_count = Var_uint(inputs_count)
        self.inputs = Var_array(inputs)
        self.outputs_count = Var_uint(outputs_count)
        self.outputs = Var_array(outputs)
        
        
    def __str__(self):
        output = "transaction:\n"
        output +="  version: " + str(self.version) + "\n"
        output +="  inputs: " + str(self.inputs) + "\n"
        output +="  outputs: " + str(self.outputs) + "\n"
        return output
        
        
    def encode(self):
        
        debut = self.version.encode() + self.flags_count.encode() + self.flags.encode()
        milieu = self.inputs_count.encode() + self.inputs.encode()
        fin = self.outputs_count.encode() + self.outputs.encode()
        
        return debut + milieu + fin
        
        
        
class Tx_in:
    
    def __init__(self, previous_output, script_length, script):
                     
        self.previous_output = Outpoint(previous_output)
        self.script_length = Var_uint(script_length)
        self.script = Var_array(script)

        
    def __str__(self):
        output = "tx_in:\n"
        output +="  previous_output: " + str(self.previous_output) + "\n"
        output +="  script_length: " + str(self.script_length) + "\n"
        output +="  script: " + str(self.script) + "\n"
        return output
        
        
    def encode(self):
        return self.previous_output.encode() + self.script_length.encode() + self.script.encode()



class Tx_out:
    
    def __init__(self, value, script_length, script):
                     
        self.value = Uint64(value)
        self.script_length = Var_uint(script_length)
        self.script = Var_array(script)

        
    def __str__(self):
        output = "tx_out:\n"
        output +="  value: " + str(self.value) + "\n"
        output +="  script_length: " + str(self.script_length) + "\n"
        output +="  script: " + str(self.script) + "\n"
        return output
        
        
    def encode(self):
        return self.previous_output.encode() + self.script_length.encode() + self.script.encode()
        
        
        
class Outpoint:

    def __init__(self, t_hash, index):
                     
        self.hash = Finite_string(t_hash)
        self.index = Uint32(index)

        
    def __str__(self):
        output = "outpoint:\n"
        output +="  hash: " + str(self.hash) + "\n"
        output +="  index: " + str(self.index) + "\n"
        return output
        
        
    def encode(self):
        return self.hash.encode() + self.index.encode()
        
        
        
class Getblocks():

    def __init__(self, count, locator, b_hash):
                     
        self.count = Var_uint(count)
        self.locator = Finite_string(locator)
        self.hash = Finite_string(b_hash)

        
    def __str__(self):
        output = "getblocks:\n"
        output +="  count: " + str(self.count) + "\n"
        output +="  locator: " + str(self.locator) + "\n"
        output +="  hash: " + str(self.hash) + "\n"
        return output
        
        
    def encode(self):
        return self.count.encode() + self.locator.encode() + self.hash.encode()





a = Message("inv",8,"a")
print(a.encode())
print(decode_message(a.encode()))