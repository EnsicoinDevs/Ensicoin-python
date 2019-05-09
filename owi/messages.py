#!/usr/bin/env python3
"""
Created on Thu Nov 15 19:34:19 2018

@author: Admin
"""

import translator

def whoami():
    """
    returns a compatible whoami so it can be sent to another node
    """
    addr = translator.Address()
    addr.create()
        
    payload = translator.Whoami()
    payload.create(1,addr,2,[translator.Var_str("node")])
    paie = payload.encode()
    l = len(paie)
    
    a=translator.Message()
    a.create("whoami",l,paie)
    message = a.encode()
    
    return message


def whoamiack():
    paie = ""
    l = 0
    a=translator.Message()
    a.create("whoamiack",l,paie)
    message = a.encode()
    
    return message
