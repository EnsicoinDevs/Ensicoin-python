# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 01:21:49 2018
@author: jonathan
"""

import hashlib


class script_interpreter:
    
    def __init__(self): #script est une liste
    
        """
        initialize the interpreter
        """
        
    def main(self,script):
        
        """
        main method of the interpreter.
        it runs the script and return whether the transaction is valid or not
        
        the memory only has 100 registers and the first is used for command results
        the maximum total number of instructions executed is 1000
        """
        self.memory = [0 for k in range(100)] #memory[0] acceuille les resultats
        self.is_valid = False
        self.position = 0 
        self.limite= 1000 #limite d'instructions executées
        self.nb_iterations = 0
        
        l=len(script)
        while self.position < l and self.nb_iterations < self.limite:
            
            line = script[self.position]
            self.position += 1
            self.nb_iterations +=1
            
            if line[0]=="set":
                self.s_set(line[1],line[2])
            if line[0]=="copy":
                self.s_copy(line[1],line[2])
            if line[0]=="add":
                self.s_add(line[1],line[2])
            if line[0]=="sub":
                self.s_sub(line[1],line[2])
            if line[0]=="mult":
                self.s_mult(line[1],line[2])
            if line[0]=="div":
                self.s_div(line[1],line[2])
            if line[0]=="and":
                self.s_and(line[1],line[2])
            if line[0]=="or":
                self.s_or(line[1],line[2])
            if line[0]=="not":
                self.s_not(line[1])
            if line[0]=="xor":
                self.s_xor(line[1],line[2])
            if line[0]=="equal":
                self.s_equal(line[1],line[2])
            if line[0]=="sup":
                self.s_sup(line[1],line[2])
            if line[0]=="goto":
                self.s_goto(line[1],line[2])
            if line[0]=="return":
                self.position = l
            if line[0]=="valid":
                self.is_valid = True
                self.position = l
            if line[0]=="hash":
                self.s_hash(line[1])
                
        return self.is_valid
                
        
    def s_set(self,adresse,valeur):
        """
        sets the memory address "adresse" to the value "valeur"
        """
        self.memory[adresse] = valeur
        
    def s_copy(self,source,destination):
        """
        copies the value of the "source" memory address to the "destination" adress
        """
        self.memory[destination] = self.memory[source]
    
    def s_add(self,a,b):
        """
        puts A+B at address 0
        A and B designate the content of the addresses a and b
        """
        self.memory[0] = self.memory[a] + self.memory[b]
        
    def s_sub(self,a,b):
        """
        puts A-B at address 0
        A and B designate the content of the addresses a and b
        """
        self.memory[0] = self.memory[a] - self.memory[b]
        
    def s_mult(self,a,b):
        """
        puts A*B at address 0
        A and B designate the content of the addresses a and b
        """
        self.memory[0] = self.memory[a] * self.memory[b]
        
    def s_div(self,a,b):
        """
        puts A/B at address 0
        A and B designate the content of the addresses a and b
        """
        self.memory[0] = self.memory[a] / self.memory[b]
        
    def s_and(self,a,b):
        """
        puts (A and B) at address 0 (returns 0 or 1)
        A and B designate the content of the addresses a and b
        """
        self.memory[0] = self.memory[a] and self.memory[b]
        
    def s_or(self,a,b):
        """
        puts (A or B) at address 0 (returns 0 or 1)
        A and B designate the content of the addresses a and b
        """
        self.memory[0] = self.memory[a] or self.memory[b]
        
    def s_not(self,a):
        """
        puts (not A) at address 0 (returns 0 or 1)
        A designates the content of the address a
        """
        self.memory[0] = int(not(self.memory[a]))
        
    def s_xor(self,a,b):
        """
        puts (A xor B) at address 0 (returns 0 or 1)
        A and B designate the content of the addresses a and b
        """
        self.memory[0] = (a and not(b)) or (not(a) and b)
        
    def s_equal(self,a,b):
        """
        puts (A == B) at address 0 (returns 0 or 1)
        A and B designate the content of the addresses a and b
        """
        self.memory[0] = int(self.memory[a] == self.memory[b])
        
    def s_sup(self,a,b):
        """
        puts (A > B) at address 0 (returns 0 or 1)
        A and B designate the content of the addresses a and b
        """
        self.memory[0] = int(self.memory[a] > self.memory[b])
        
    def s_goto(self,adresse_booleen,position_saut):
        """
        jumps to the "position_saut" location in the script if the value of "adresse_booleen" is evaluated as True
        """
        if self.memory[adresse_booleen]:
            self.position = position_saut
        
    def s_hash(self,a):
        """
        puts the hash of A in memory address 0
        A designates the content of the address a
        """
        self.memory[0] = hashlib.md5(str(a).encode()) 
        
        
c=script_interpreter()
script=[["set",1,40],["set",2,2],["add",1,2],["set",3,42],["equal",0,3],["not",0,0],["goto",0,8],["valid",0,0],["return",0,0]] 
print(c.main(script))
