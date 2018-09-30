# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 20:42:38 2018

@author: jonathan
"""

import tkinter as tk
import requests
import json
import datetime

nom  = ""

class InterfaceMDP(tk.Frame):

    def __init__(moi,f):

        moi.nom = tk.StringVar()
        moi.nom.set("")
        moi.mdp = tk.StringVar()
        moi.mdp.set("")
        moi.f=f

        tk.Frame.__init__(moi,f)
        moi.pack()

        moi.label_nom = tk.Label(moi, text = "nom",font=('Calibri', 15))
        moi.label_nom.pack()
        
        moi.entree_nom = tk.Entry(moi, textvariable=moi.nom, width=30,font=('Calibri', 15))
        moi.entree_nom.pack()

        moi.label_mdp = tk.Label(moi, text = "mot de passe",font=('Calibri', 15))
        moi.label_mdp.pack()
        
        moi.entree_mdp = tk.Entry(moi, textvariable=moi.mdp, width=30,font=('Calibri', 15))
        moi.entree_mdp.pack()

        moi.bouton_valider = tk.Button(moi, text="valider", font=('Calibri', 15), command = moi.valider)
        moi.bouton_valider.pack()
        return

    def valider(moi):
        global nom
        if moi.nom.get()=="jonathan" and moi.mdp.get()=="12345":
            nom = moi.nom.get()
            moi.f.destroy()
        return

class Interface(tk.Frame):

    def __init__(moi,f):
        global nom
        print(nom)
        moi.liste_transactions = []
        moi.destinataire = tk.StringVar()
        moi.destinataire.set("")
        moi.montant = tk.IntVar()
        moi.montant.set(0)
        moi.possession = 0
        moi.nom = nom
        
        moi.deroulement = 0
    
        
        tk.Frame.__init__(moi,f)
        moi.pack()
        
        #moi.bandeau_superieur = tk.Frame(moi,borderwidth=3, relief = tk.GROOVE)
        #moi.bandeau_superieur.pack(side=tk.TOP, padx=0, pady=0)
        
        moi.transactions_frame = tk.Frame(moi, borderwidth=2, relief=tk.GROOVE)
        moi.transactions_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        moi.virements_frame = tk.Frame(moi, borderwidth=2, relief=tk.GROOVE)
        moi.virements_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        moi.sousous = tk.Label(moi.virements_frame, text = "Ensicoins possédés: ",font=('Calibri', 15))
        moi.sousous.pack()

        moi.sous = tk.Label(moi.virements_frame, text = "",font=('Calibri', 15))
        moi.sous.pack()
        
        moi.bouton_recharger = tk.Button(moi.virements_frame, text="actualiser les transactions",font=('Calibri', 17) , command=moi.recharger)
        moi.bouton_recharger.pack(pady=20)
        
        moi.c = tk.Canvas(moi.transactions_frame, width=400, height=300, background='white')
        moi.tc=[moi.c.create_text(200,k*20+20,text = "",font=('Calibri', 15)) for k in range(14)]
        moi.c.pack()
        
        moi.label_destinataire = tk.Label(moi.virements_frame, text = "destinataire",font=('Calibri', 15))
        moi.label_destinataire.pack()
        
        moi.entree_destinataire = tk.Entry(moi.virements_frame, textvariable=moi.destinataire, width=30,font=('Calibri', 15))
        moi.entree_destinataire.pack()  
        
        moi.label_montant = tk.Label(moi.virements_frame, text = "montant",font=('Calibri', 15))
        moi.label_montant.pack()
        
        moi.entree_montant = tk.Entry(moi.virements_frame, textvariable=moi.montant, width=30,font=('Calibri', 15))
        moi.entree_montant.pack() 
        
        moi.bouton_envoi = tk.Button(moi.virements_frame, text = "effectuer la transaction", font = ('Calibri', 15), command = moi.virement)
        moi.bouton_envoi.pack(pady = 10)
        
        moi.bouton_haut = tk.Button(moi.virements_frame,text = "monter", font = ('Calibri', 15), command = moi.derouler_haut )
        moi.bouton_haut.pack(pady = 20)
        
        moi.bouton_bas = tk.Button(moi.virements_frame,text = "descendre", font = ('Calibri', 15), command = moi.derouler_bas )
        moi.bouton_bas.pack()

        moi.recharger()
        return
        
    def recharger(moi):
        
        #noeud = requests.get("http://nom_du_site_hebergeant le noeud.org/")
    
        #------provisoire-----------
        with open('donnees.json') as json_data:
            donnees = json.load(json_data)
        moi.liste_transactions = donnees["transactions"]
        #---------------------------
        
        if moi.deroulement > len(moi.liste_transactions)-14:
            moi.deroulement = len(moi.liste_transactions)-14
        if moi.deroulement < 0:
            moi.deroulement = 0
        
        a=0
        for ligne in moi.liste_transactions[moi.deroulement:14+moi.deroulement]:
            moi.c.itemconfig(moi.tc[a],text=str(ligne[0]) + ":" + str(ligne[1]) + ":" + str(ligne[2]) + " ,  " + ligne[3] + " -> " + ligne[4] + " : " +str(ligne[5]))
            a+=1

        moi.calcul()
        
        return
        
    def virement(moi):
        
        date = datetime.datetime.now()
        
        data = {"transaction": [date.day, date.month, date.year, moi.nom, moi.destinataire.get(), moi.montant.get()]}
        #requests.post("http://nom_du_site_hebergeant le noeud.org/", data = data)
        
        #provisoire        
        print(data)
        #----------
        return
        
    def derouler_bas(moi):
        moi.deroulement += 1
        moi.recharger()
        return
        
    def derouler_haut(moi):
        if moi.deroulement > 0:
            moi.deroulement += -1
        moi.recharger()
        return

    def calcul(moi):
        moi.possession = 0
        for ligne in moi.liste_transactions:
            if ligne[3] == moi.nom:
                moi.possession += -1*ligne[5]
            if ligne[4] == moi.nom:
                moi.possession += ligne[5]
        moi.sous.config(text=str(moi.possession))
        
        
f1=tk.Tk()
f1.title("Ensicoin Wallet Login")

interface = InterfaceMDP(f1)

f1.mainloop()
        
        

f2=tk.Tk()
f2.title("Ensicoin Wallet")

interface = Interface(f2)

f2.mainloop()
