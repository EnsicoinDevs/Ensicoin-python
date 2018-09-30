# ensicoin-script

premier jet avec les fonctions

set
<br/>copy
<br/>add
<br/>sub
<br/>mult
<br/>div
<br/>and
<br/>or
<br/>not
<br/>xor
<br/>equal
<br/>sup
<br/>goto
<br/>return
<br/>valid
<br/>hash


<br/><h4>on peut par exemple faire des conditionelles avec</h4>

  ...test... --> resultat à l'adresse 0
  <br/>n)    not 0 ?
  <br/>n+1)  goto 0 "n+k" <-- c'est une adresse
  <br/>n+2)  ... contenu de la conditionelle
  <br/>n+3)  ...
  <br/>... 
  <br/>n+k-1)... fin de la conditionelle
  <br/>n+k)  ... on reprend après la conditionelle
  
  
<br/><h4>et des boucles "while" avec</h4>

  ...test... --> resultat à l'adresse 0
  <br/>n)    not 0 ?
  <br/>n+1)  goto 0 "n+k+1" 
  <br/>n+2)  ... contenu de la boucle
  <br/>n+3)  ...
  <br/>... 
  <br/>n+k-1)... test pour reboucler
  <br/>n+k)  goto 0 "n+2"
  <br/>n+k+1)... on continue
  
  <br/>le code doit se presenter en entrée comme une liste d'instructions de 3 termes:
  <br/>par exemple: 
  <br/>[["set",1,40],["set",2,2],["add",1,2],["set",3,42],["equal",0,3],["not",0,0],["goto",0,8],["valid",0,0],["return",0,0]]
  <br/>renvoie True, car 40 + 2 = 42, mais
  <br/>[["set",1,40],["set",2,3],["add",1,2],["set",3,42],["equal",0,3],["not",0,0],["goto",0,8],["valid",0,0],["return",0,0]]
  <br/>renvoie False car 40 + 3 = 43, different de 42
