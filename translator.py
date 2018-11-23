# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 12:48:04 2018

@author: julouj
"""
MAGIC = 422021
conversion_table = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 
             'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 
             'Q', 'R', 'S', 'T', 'U', 'V')

def triacontakai(n):
    print(list(conversion_table[int(k)] for k in str(n)))
    return sum(conversion_table[int(k)] for k in str(n))

def build_message(m_type,m_length,payload):
    magic = triacontakai(MAGIC)
    length = triacontakai(m_length)
    m_type = m_type + " "*(12-len(m_type))
    return magic + m_type + length + payload
    
def decode_message(message):
    magic = message[0:4]
    m_type = message[4:16]
    m_length = int(message[16:20],16)
    payload = message[20:]
    return magic,m_type,m_length,payload
    
a = build_message("inv         ",8,"a")
print(a)
print(decode_message(a))