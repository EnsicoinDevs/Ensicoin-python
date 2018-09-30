# ensicoin-wallet-client-python

transactions au format json:

sortie:
  "transaction" : [jour,mois,année,emetteur,destinataire,montant]
  
entrée:
  "transactions" : [transaction1,transaction2,...]

il manque les interactions avec le serveur et les contre-mesures de bugs possibles.

le login devrait-il etre verifié par le serveur, ou bien prefererais-t-on un systeme où n'importe qui peut voir les transactions des autres sans mot de passe, mais ce dernier est necessaire pour faire une transaction valide ?
