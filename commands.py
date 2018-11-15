# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 20:31:23 2018

@author: Admin
"""


def command_dict():
    return {"help":command_help,
            "connections":command_connections
            }
            
def help_dict():
    return {"help":help_help,
            "connections":help_connections
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
            print('Connected to {}:{}'.format(TCP_IP, TCP_PORT))
        except:
            print("wrong address format")
    else:
        print("unknown argument: " + str(command[1]))
        
def help_connections():
    print("command used for all things networking")
    print("format: connections [func] {args}")
    print("possible functions:")
    print("   set :   TCP_IP   TCP_PORT")
