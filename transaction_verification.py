# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 13:11:12 2018

@author: julouj
"""

import script_pile

MAX_BLOCK_SIZE = 42 


def transaction_verif(transaction,is_at_block_beginning):
    
    #-----------------verification of json format------------------------------
    if "version" in transaction and "flags" in transaction and "inputs" in transaction and "outputs" in transaction:
        t_inputs = transaction["inputs"]
        t_outputs = transaction["outputs"]
        
        POs = []
        input_scripts = []
        values = []
        output_scripts = []

        for t_input in t_inputs:
            if "previousOutput" in t_input and "script" in t_input:
                POs.append(t_input["previousOutput"])
                input_scripts.append(t_input["script"])
            
                if "transactionHash" in t_input["previousOutput"] and "index" in t_input["previousOutput"]:
                    t_hash = t_input["previousOutput"]["transactionHash"]
                    index = t_input["previousOutput"]["index"]  #useless affectations to verify
                
                else:
                    return False
            
            else:
                return False
        
        for t_output in t_outputs:
            if "value" in t_output and "script" in t_output:
                values.append(t_output["value"])
                output_scripts.append(t_output["script"])
            
            else:
                return False
        
    else:
        return False
    #-----------------verification of json format------------------------------
    
    #-----------------at least 1 input and output------------------------------
    if len(t_inputs)<=0 and len(t_outputs)<=0:
        return False
    #-----------------at least 1 input and output------------------------------
        
    #-----------------size <= MAX_BLOCK_SIZE-----------------------------------
        #ASK JOHYN HOW TO CALCULATE SIZE
    #-----------------size <= MAX_BLOCK_SIZE-----------------------------------
    
    #-----------------output values > 0----------------------------------------
    for value in values:
        if value <= 0:
            return False
    #-----------------output values > 0----------------------------------------
            
    #-----------------coinbase verification------------------------------------
    if not(is_at_block_beginning) and len(t_inputs) == 0:
        return False
    #-----------------coinbase verification------------------------------------
    
    #-----------------sum input > sum outputs----------------------------------
    input_values = []
    for PO in POs:
        
    
    sum(values)<

    #-----------------sum input > sum outputs----------------------------------
    
    
    
    
    
    
    
    
    
    
    
    
    
    