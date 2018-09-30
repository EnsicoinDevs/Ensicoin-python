# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 13:09:38 2018
@author: julouj
"""

import hashlib

from ecdsa import VerifyingKey, SECP256k1

class script_interpreter:

    def __init__(self):

        """
        initialize the interpreter
        """

    def main(self,script): #script est une liste

        """
        main method of the interpreter.
        it runs the script and return whether the transaction is valid or not
        """

        if str(type(script)) != "<class 'list'>":
            return False #test du type du script -> False si non liste

        self.stop = False
        self.pile = [] #la pile de sockage des donnees
        self.is_valid = True

        dicommande = {"OP_DUP":self.OP_DUP,"OP_HASH160":self.OP_HASH160,"OP_EQUAL":self.OP_EQUAL,"OP_AND":self.OP_AND,"OP_OR":self.OP_OR,"OP_NOT":self.OP_NOT,"OP_ADD":self.OP_ADD,"OP_OPPOSITE":self.OP_OPPOSITE,"OP_MULT":self.OP_MULT,"OP_DIV":self.OP_DIV,"OP_VERIFY":self.OP_VERIFY,"OP_CHECKSIG":self.OP_CHECKSIG}

        for ligne in script:

            if ligne[-1]=="\n":
                ligne = ligne[:-1]

            if ligne in dicommande:
                dicommande[ligne]()

            else:
                caractere=ligne[0]
                compte=0
                valeur=""
                type_valeur=""

                while caractere != " ":
                    type_valeur=type_valeur + caractere
                    compte+=1
                    caractere = ligne[compte]

                if len(ligne)>compte+1:
                    valeur = ligne[compte+1:]  #valeur est deja un string, donc on ignore le type string
                else:
                    valeur = ligne  #permet de definir des strings sans marquer STRING devant si on veut

                if type_valeur == "INT":
                    valeur = int(valeur)

                if type_valeur == "BOOL":
                    if valeur == "True":
                        valeur = True
                    else:
                        valeur = False

                if type_valeur == "FLOAT":
                    valeur = float(valeur)

                self.pile.append(valeur)

            if self.stop:
                break

        return self.is_valid

    def OP_DUP(self):
        """
        Duplique le haut de la pile.
        """
        dernier = self.pile.pop() #pop supprime le haut de la pile
        self.pile.append(dernier)
        self.pile.append(dernier)
        
    def OP_HASH160(self):
        """
        Hash le haut de la pile avec RIPEMD-160.
        """
        dernier = self.pile.pop()
        try:
            self.pile.append(hashlib.ripemd160(str(dernier).encode()))
        except:
            return False

    def OP_EQUAL(self):
        """
        Remplace les deux valeurs du haut de la pile par vrai si elles sont égales,
        par faux sinon.
        """
        a=self.pile.pop()
        b=self.pile.pop()
        self.pile.append(a==b)

    def OP_AND(self):
        """
        Remplace les deux valeurs du haut de la pile par vrai si elles sont vraies,
        par faux sinon.
        """
        a=self.pile.pop()
        b=self.pile.pop()
        self.pile.append(a and b)

    def OP_OR(self):
        """
        Remplace les deux valeurs du haut de la pile par vrai si l'une est vraie,
        par faux sinon.
        """
        a=self.pile.pop()
        b=self.pile.pop()
        self.pile.append(a or b)

    def OP_NOT(self):
        """
        Remplace la valeur du haut de la pile par son oppose booleen,
        """
        haut=self.pile.pop()
        self.pile.append(not(haut))

    def OP_ADD(self):
        """
        Remplace les deux valeurs du haut de la pile par leur somme,
        """
        a=self.pile.pop()
        b=self.pile.pop()
        self.pile.append(a+b)

    def OP_OPPOSITE(self):
        """
        Remplace la valeur du haut de la pile par son opposé (flottant),
        """
        a=self.pile.pop()
        try:
            self.pile.append(-1*float(a))
        except:
            return False

    def OP_MULT(self):
        """
        Remplace les deux valeurs du haut de la pile par leur produit (flottant),
        """
        a=self.pile.pop()
        b=self.pile.pop()
        try:
            self.pile.append(float(a)*float(b))
        except:
            return False

    def OP_DIV(self):
        """
        Remplace les deux valeurs du haut de la pile par leur fraction (flottante),
        """
        a=self.pile.pop()
        b=self.pile.pop()
        try:
            self.pile.append(float(a)/float(b))
        except:
            return False

    def OP_VERIFY(self):
        """
        Marque la transaction comme invalide si le haut de la pile est à faux,
        enlève le haut de la pile sinon.
        """
        self.is_valid = bool(self.pile.pop())
        self.stop = True

    def OP_CHECKSIG(self):
        """
        Utilise la clé publique qui est en haut de la pile pour vérifier que
        la signature située juste en-dessous est valide.
        Marque la transaction comme invalide sinon.
        Enlève ces deux valeurs de la pile.
        """
        pubkey = self.pile.pop()
        sig = self.pile.pop()
        try:
            vk = VerifyingKey.from_string(bytes.fromhex(pubkey), curve=SECP256k1)
            self.is_valid = vk.verify(bytes.fromhex(sig), bytes.fromhex(pubkey), hashlib.sha256)
        except:
            return False


"""
prog = open("programme.txt")

script=[]
for ligne in prog:
    script.append(ligne)

I=script_interpreter()

print(I.main(script))
"""
