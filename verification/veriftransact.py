# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 10:34:58 2018

@author: julouj
"""

import json
import script_pile

MAX_BLOCK_SIZE = 42  #inutilisé pour le moment

def veification_transaction(est_debut_bloc):
    
    try:#on teste si c'est bien du json correct
        with open("transaction.json", "r") as file:
            data = json.load(file)
    except:
        return False
        
        
    #-----------------verification du contenu du json-------------------------------------
    if "version" in data and "flags" in data and "inputs" in data and "outputs" in data:
        entrees = data["inputs"]
        sorties = data["outputs"]
        
        POs = []
        scripts_entrees = []
        valeurs = []
        scripts_sorties = []

        for entree in entrees:
            if "previousOutput" in entree and "script" in entree:
                PO.append(entree["previousOutput"])
                script_entree.append(entree["script"])
            
                if "transactionHash" in PO and "index" in PO:
                    t_hash = PO["transactionHash"]
                    indice = PO["index"]   #affectations inutiles, juste pour verification
                
                else:
                    return False
            
            else:
                return False
        
        for sortie in sorties:
            if "value" in sortie and "script" in sortie:
                valeurs.append(sortie["value"])
                script_sortie.append(sortie["script"])
            
            else:
                return False
        
    else:
        return False
    #-----------------verification du contenu du json-------------------------------------
    
    #-----------------verification de la taille ------------------------------------------
    # je sais pas quoi faire là
    #-----------------verification de la taille ------------------------------------------
    
    #-----------------verification de la valeur ------------------------------------------
    somme=0
    for valeur in valeurs:
        if valeur > 0:
            somme+=valeur
        else:
            return False
    #-----------------verification de la valeur ------------------------------------------
    
    #-----------------verification coinbase ----------------------------------------------
    if not(est_debut_bloc) and len(entrees) == 0:
        return False
    #-----------------verification coinbase ----------------------------------------------
    
    #-----------------verification somme sortie/entree -----------------------------------
    
    #La somme des sorties doit être strictement inférieure à celle des entrées
    #mais il n'y a pas de valeur en entree :( on reutilisera la variable somme
    
    #-----------------verification somme sortie/entree -----------------------------------
    
    # 7,8,9,10,11 : implementer la blockchain et le pool d'abord
    
    #-----------------verification script-------------------------------------------------
    
    if len(entrees) != 0:
        I=script_pile.script_interpreter()
        # je suis pas sur d'avoir bien compris comment c'etait censé fonctionner là ...
        for entree,script_entree in entrees,scripts_entrees:
            for sortie,script_sortie in sorties,scripts_sorties:
                programme = script_sortie + script_entree #concatenation des scripts
                if not(I.main(programme)):
                    return False
    else: #cas d'une coinbase
        for sortie,script_sortie in sorties,scripts_sorties:
            programme = script_sortie
            if not(I.main(programme)):
                return False
        
             
    #-----------------verification script-------------------------------------------------
    
    return True #le reste se ferait dans un proramme separé ?
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
