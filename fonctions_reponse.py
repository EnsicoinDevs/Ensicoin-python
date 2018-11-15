# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 20:17:05 2018

@author: Admin
"""

import json
from gestionnaire_blocs import *


def type_dict():
    return {"whoami" : ans_whoami,
            "inv" : ans_inv,
            "notfound" : ans_notfound,
            "getdata" : ans_getdata,
            "block" : ans_block,
            "transaction" : ans_transaction,
            "getblocks" : ans_getblocks,
            "getmempool" : ans_getmempool
            }


def ans_whoami():
    C.send(name,"wtf, tu m'as deja dit bonjour")


def ans_inv(message,name,C):
    data_type = message["type"]
    data = message["hashes"]
    unknown_list = []
    known_list = []
    
    if data_type == "b":
        
        for block in data:
            try:
                get_block(block)
                known_list.append(block)
            except:
                unknown_list.append(block)
                
        send_getdata(unknown_list,data_type,name,C)
    
        for blockhash in unknown_list:
            ans = C.listen(name)
            if ans["type"]!="notfound":
                add_block(ans["message"],blockhash)
            
    if data_type == "t":
        
        for transact in data:
            test = is_transaction_in_a_block(transact)
            if test:
                known_list.append(transact)
            else:
                unknown_list.append(transact)
                
        send_getdata(unknown_list,data_type,name,C)
    
        for transacthash in unknown_list:
            ans = C.listen(name)
            if ans["type"]!="notfound":
                add_transact(ans["message"],transacthash)
        
    else:
        print("error: wrong type in inv")
        C.send(name,"what the shit are you talking to me: wrong type in inv")
        C.end_connexion(name)
        return []
        
        
def ans_notfound(message,name,C):
    return 0
    
def ans_getdata(message,name,C):
    
    data_type = message["type"]
    data = message["hashes"]
    
    if data_type == "b":
        
        for block_hash in data:
            try:
                block = get_block(block_hash)
                send_block(block,name,C)
            except:
                send_notfound(data_type,name,C)
            
    if data_type == "t":
        for transact_hash in data:
            try:
                transact = find_transaction(transact_hash)
                send_transaction(transact,name,C)
            except:
                send_notfound(data_type,name,C)
        
        
    else:
        print("error: wrong type in inv (getdata)")
        C.send(name,"what the shit are you talking to me: wrong type in inv")
        C.end_connexion(name)
        return []  
    
def ans_block(message,name,C):
    return 0
    
def ans_transaction(message,name,C):
    return 0
    
def ans_getblocks(message,name,C):
    
    block_list = list(block["hash"] for block in iter_blocks())
    
    msg = msg_template()
    msg["type"] = "inv"
    msg["message"] = {"type":"b","hashes":block_list}
    C.send(name,msg)
    
def ans_getmempool(message,name,C):
    
    transact_list = list(transact["hash"] for transact in iter_transaction_that_isnt_in_a_block())
    
    msg = msg_template()
    msg["type"] = "inv"
    msg["message"] = {"type":"t","hashes":transact_list}
    C.send(name,msg)
    
    
    
    
def send_getdata(unknown_list,data_type,name,C):
    msg = msg_template()
    msg["type"] = "inv"
    msg["message"] = {"type":data_type,"hashes":unknown_list}
    C.send(name,msg)
    
def send_notfound(data_type,name,C):
    msg = msg_template()
    msg["type"] = "notfound"
    msg["message"] = {"type":data_type,"hash":""}
    C.send(name,msg)
    
def send_block(block,name,C):
    msg = msg_template()
    msg["type"] = "block"
    msg["message"] = block
    C.send(name,msg)
    
def send_transaction(transact,name,C):
    msg = msg_template()
    msg["type"] = "transaction"
    msg["message"] = transact
    C.send(name,msg)
    
    
    
def msg_template():
    """
    returns the template of a message compatible with the protocol
    the dictionnary "message" is empty so it can be filled later
    """
    
    f=open("msg_template.json", "r")
    data = json.load(f)
    f.close()
    return data
    
    
    
    
    
    
    
    
    
    
    
    
    