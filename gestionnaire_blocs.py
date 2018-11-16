# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 14:19:45 2018
@author: Admin
"""

import json
import hashlib


def add_block(block_hash,block):
    """
    creates a new block in the blockchain
    """
    
    try:
        chain_length = get_block_chain_length(block["header"]["hashPrevBlock"])+1
    except:
        chain_length = 1
    
    bhash = calculate_block_hash(block["header"])
    
    towrite = {"block":block,"hash":bhash,"chain_length":chain_length}
    
    file=open("blockchain/{}.json".format(block_hash), "w")
    data = json.dumps(towrite)
    file.write(data)
    file.close()

def get_block(block_hash):
    """
    returns the content of a block as a hashtable extracted from the json
    """
    
    block=open("blockchain/{}.json".format(block_hash), "r")
    data = json.load(block)
    block.close()
    
    if data["hash"] == str(block_hash):
        return data["block"]
    else:
        print("storage error: wrong hash in database")
        return False


def get_block_chain_length(block_hash):
    """
    returns the length of the chain the block is in
    """
    
    block=open("blockchain/{}.json".format(block_hash), "r")
    data = json.load(block)
    block.close()
    
    if data["hash"] == str(block_hash):
        return data["chain_length"]
    else:
        print("storage error: wrong hash in database")
        return False


def calculate_block_hash(block_header):
    """
    takes in a block header which is a hashtable and returns its hash
    """
    steak = "" 
    
    steak += str(block_header["version"])
    for flag in  block_header["flags"]:
        steak += str(flag)
    
    steak += str(block_header["hashPrevBlock"])
    steak += str(block_header["hashTransactions"])
    steak += str(block_header["timestamp"])
    steak += str(block_header["nonce"])
    
    steak_hashe = hashlib.sha256(steak.encode())
    steak_hashe = hashlib.sha256(steak_hashe.digest())

    return steak_hashe.hexdigest()
    
    
def transaction_hash(transaction):
    """
    returns the hash of the transaction (which is a hashtable)
    """
    steak = "" 
    
    steak += str(transaction["version"])
    
    for flag in  transaction["flags"]:
        steak += str(flag)
    
    for t_input in  transaction["inputs"]:
        #transactionHash, index et script
        steak += str(t_input["previousOutput"]["transactionHash"])
        steak += str(t_input["previousOutput"]["index"])
        steak += str(t_input["script"])
        
    for t_output in transaction["outputs"]:
        steak += str(t_output["value"])
        steak += str(t_output["script"])
    
    steak_hashe = hashlib.sha256(steak.encode())
    steak_hashe = hashlib.sha256(steak_hashe.digest())

    return steak_hashe.hexdigest()
    

def transaction_signature(transaction):
    """
    returns the signature of the transaction (which is a hashtable)
    """
    steak = "" 
    
    steak += str(transaction["version"])
    
    for flag in  transaction["flags"]:
        steak += str(flag)
    
    for t_input in  transaction["inputs"]:
        #transactionHash, index et script
        steak += str(t_input["transactionHash"])
        steak += str(t_input["index"])
        
    for t_output in transaction["outputs"]:
        steak += str(t_input["value"])
        steak += str(t_input["script"])
    
    steak_hashe = hashlib.sha256(steak.encode())
    steak_hashe = hashlib.sha256(steak_hashe.digest())

    return steak_hashe.hexdigest()
        
    
    
def calculate_transactions_hash(transactions):
    """
    takes in a list of transactions and returns its hash
    """
    steak = "" 
    
    for t in  transactions:
        steak += transaction_hash(t)
        
    
    steak_hashe = hashlib.sha256(steak.encode())
    steak_hashe = hashlib.sha256(steak_hashe.digest())

    return steak_hashe.hexdigest()


def find_block(transaction_hash):
    """
    returns the hash of the block containing the transaction output
    """
    
    index=open("index.json", "r")
    data = json.load(index)
    index.close()

    return data[transaction_hash]


def get_transaction():
    """
    returns the first transaction in the mempool and removes it from it
    """
    
    mempool = open("mempool.json", "r")
    data = json.load(mempool)
    mempool.close()
    
    file = data["transactions"]
    
    if file != {}:
        
        transaction = 0
        t_hash = ""
        
        for t in file:
            transaction = file[t]
            t_hash = t
            
        del(data["transaction"][t_hash])
        
        mempool = open("mempool.json", "w")
        data = json.dumps(mempool)
        mempool.write(data)
        mempool.close()
        
        return transaction
    else:
        return False
        
def find_transaction(transaction_hash):
    """
    returns a transaction from the mempool
    """
    
    mempool = open("mempool.json", "r")
    data = json.load(mempool)
    mempool.close()
    
    file = data["transactions"]
    if transaction_hash in file:
        return file[transaction_hash]
    else:
        return None
        

def add_transaction(transactionhash,transaction):
    """
    adds a transaction to the mempool
    """
    
    mempool = open("mempool.json", "r")
    data = json.load(mempool)
    mempool.close()
    
    data["transactions"][transactionhash] = transaction 
    
    file=open("mempool.json", "w")
    msg = json.dumps(data)
    file.write(msg)
    file.close()


def iter_blocks():
    """
    iterates on the block hashes in index.json 
    """
    
    index = open("index.json", "r")
    data = json.load(index)
    index.close()
    
    for transaction_hash in data:
        yield data[transaction_hash]
        
        
def is_transaction_in_a_block(t_hash):
    """
    returns whether a transaction hash is in index.json
    """
    
    index = open("index.json", "r")
    data = json.load(index)
    index.close()
    
    return t_hash in data
    
    
def iter_transaction_that_isnt_in_a_block():
    """
    iterates on the couple (transaction,hash) where th hash is not in index.json
    """
    transaction = get_transaction()
    while transaction:
        
        t_hash = transaction_hash(transaction)
        if not is_transaction_in_a_block(t_hash):
            yield transaction,t_hash
        transaction = get_transaction()








