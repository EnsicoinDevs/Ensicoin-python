# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 20:31:23 2018

@author: Admin
"""

import json
from hlfunc import *
from fonctions_reponse import *

def command_dict():
    return {"help":command_help,
            "connections":command_connections,
            "init":command_init
            }
            
def help_dict():
    return {"help":help_help,
            "connections":help_connections,
            "init":help_init
            }





def command_help(command,C):
    
    if len(command) == 1:
        
        print("commands:")
        for possible_command in command_dict():
            print("   " + possible_command)
        print()
        print("type 'help command' to get more info on how to use that command")
        
    elif command[1] in command_dict():
        help_dict()[command[1]]()
        
    else:
        print("unknown command: " + str(command[1]))
        
def help_help():
    print("offers information on how to use commands")
    print("format: help [command]")
    
    
    
def command_connections(command,C):
    
    if len(command) == 1:
        print(C)
        
    elif command[1] == "set":
        try:
            TCP_IP = command[2]
            TCP_PORT = int(command[3])
            C.start_connexion(TCP_IP,TCP_PORT)
            name = "{}:{}".format(TCP_IP, TCP_PORT)
            C.send(name,whoami())
            print(C.listen(name))
            print('Connected to ' + name)
        except:
            print("wrong address format")
            
    elif command[1] == "end":
        try:
            TCP_IP = command[2]
            TCP_PORT = int(command[3])
            name = "{}:{}".format(TCP_IP, TCP_PORT)
            C.end_connexion(name)
            print('disconnected from ' + name)
        except:
            print("wrong address format")
            
    else:
        print("unknown argument: " + str(command[1]))
        
def help_connections():
    print("command used for all things networking")
    print("format: connections [func] {args}")
    print("possible functions:")
    print("   no args: prints the list of connected nodes")
    print("   set :   TCP_IP   TCP_PORT")
    print("   end :   TCP_IP   TCP_PORT")




def command_init(command,C):
    
    try:
        for name in C.socket_table:
            send_getblocks(name,C)
            send_getmempool(name,C)
    except:
        print("unable to get blocks and mempools from connected nodes")
        
def help_init():
    print("asks the connected nodes for blocks and mempool")

