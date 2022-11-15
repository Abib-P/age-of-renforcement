# age-of-renforcement

ia project

## Etat actuel du jeu:

2 joueurs non humain:
chaque joueur a 2 unité:

- 1 unité de type "soldat" qui peut se déplacer de 1 case par tour
- 1 unité de type "town center" qui représente la vie d'un joueur (destruction = fin de la parti)

## IA :

### Qtable pour militia:

- direction de la town allié : "R ; L ; U ; D"
- direction de l’ennemi le plus proche : "O ; R ; L ; U ; D"
- direction de la town center ennemi : "R ; L ; U ; D"
- qu'est-ce que j'ai sur autour de mon agent avec comme valeur possible : "# (extrémité du terrain); O (rien); A (
  allier); TE (Town center enemy); ME (Militia enemy)"
  - donc les valuers possible sont stocker dans un tuple. ex : "(#,O,A,TE) ; (O,O,O,O) ; (O,#,O,ME) ..."

### Action dispo pour militia:

- move dans chaque direction + wait : "U, D, L, R, O (sur place)"
- faire une action impossible ne fait pas bouger l'agent
- faire un déplacement sur une unité enemy l'attaque

### Récompense

|           Reward description           | Reward |
|:--------------------------------------:|-------:|
|          un movement interdit          |   -400 |
|    se déplacer ou rester sur place     |     -2 |
|      attaquer une milice ennemie       |     -1 |
|         tuer une milice ennemy         |     25 |
|        attaquer un town center         |     -1 |
| tuer le town center (gagner la partie) |    200 |
