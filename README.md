# age-of-renforcement

ia project

## Etat actuel du jeu:

2 joueurs non humain:
chaque joueur a 2 unité:

- 1 unité de type "soldat" qui peut se déplacer de 1 case par tour
- 1 unité de type "town center" qui représente la vie d'un joueur (destruction = fin de la parti)

## IA :

#### Qtable:

- direction de l’ennemi le plus proche : "O ; R ; L ; U ; D ; RU ; RD ; LU ; LD"
- direction de la town center ennemi : "R ; L ; U ; D ; RU ; RD ; LU ; LD"
- direction de la town allié : "R ; L ; U ; D ; RU ; RD ; LU ; LD"
- est-ce que la town-center allier est plus proche que celle ennemy : "True ; False"
- qu'est-ce que j'ai sur autour de mon agent avec comme valeur possible : "# (extrémité du terrain); O (rien); A (
  allier); E (ennemi)"
  - donc les valuers possible sont stocker dans un tuple. ex : "(#,O,A,E) ; (O,O,O,O) ; (O,O,O,E) ..."
