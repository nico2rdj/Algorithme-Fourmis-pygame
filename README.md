# Algorithme des fourmis sur pygame

<p align="center" >
   <a href="">
    <img alt="react-native-gifted-chat" src="https://media.giphy.com/media/QAb8LBD8MMCn5UyNXL/giphy.gif" width="260" height="510" />
 </a>

</p>

<h3 align="center">
  🐜 Algorithme des fourmis
</h3>
<p align="center">
  Algorithme des fourmis sur l'interface pygame <br/>
  <small></small>
</p>

## Manuel d'utilisation

- Lancer la commande "python AlgorithmeFourmis.py"
- Le tracé rouge est celui avec le plus fort taux de phéromone
- Pour toutes modifications:
  - Changement de la disposition des noeuds sur l'interface pygame: Dans la classe Scene, on édite la vaiable de classe nodes_coord qui par défault est à : [(4,2), (12,2), (16,12), (12,16), (4,8)] 
  - Changement du coût des arrêtes entre les noeuds: Dans la classe Scene, on édite la variable contenant la matrice de coût edges_matrix qui par défault est à : 
   <br/>
  [0,10,20,30,15] <br/>
  [10,0,10,20,25] <br/>
  [20,10,0,10,20] <br/>
  [30,20,10,0,10] <br/>
  [15,25,20,10,0] <br/>
   <br/>
  
  - Changement des paramètres : Dans la classe Scene, on édite les variables : <br/>
    - colony_size: taille de la colonie (default: 100)
    - alpha: paramètre alpha (default: 0.5)
    - beta: paramètre beta (default: 2.0)
    - decay: taux d'oubli (default: 0.5)
    - initial_pheromone: initialisation des phéromones (default: 0.0)
    
   
    
    
    

## Détails de l'implémentation de l'algorithme des fourmis

Au niveau de l'algorithme des fourmis, plusieurs structures ont été définies. 
- Node : Elle représente un noeud du graphe
- Edge : Elle représente une arrête entre deux noeuds. Elle est caractérisée par son coût et ses phéromones. 
- Ant : Elle représente une fourmie. Elle est caractérisée par ses paramètres :
  - alpha et beta
  - Les noeuds qu'elle a visité
  - Les edges qu'elle a visité
- Scene : Elle représente le graphe des noeuds. Elle est l'endroit où l'on instancie la colonie de fourmis.Elle est caractérisée par:
  - Taille de la colonie 
  - alpha et beta 
  - Initialisation des phéromones 
  - Taux d'oublie des phéromones 
  - La matrice de coût entre les noeuds du graphe

Une brief description de l'algorithme des fourmis : 
- On crée la colonie de fourmis qui démarre au premier noeud du graphe
- La fourmie va évaluer le coût associé à chaque arrête qu'elle peut prendre en se basant sur le coût de l'arrête et sur les phéromones associées avec la formule : <br/>
![index](https://user-images.githubusercontent.com/22484369/73753986-e951ad80-4763-11ea-95c3-145cccf2d635.jpeg)
- Ensuite, la fourmie va choisir un chemin au hasard basée sur la distribution obtenue grâce à la formule ci-dessus.
- A chaque fois qu'elle visite un nouveau noeud, elle ajoute le noeud et l'arrête parcouru dans leurs listes respectives.
- Une fois tout les noeuds visités, une autre fourmie de la colonie démarre
- Une fois que toutes les fourmis de la colonie ont parcouru le graphe :
  - On applique le facteur d'oubli aux arrête du graphe
  - On update toutes les phéromones présentent sur les arrêtes avec la forume suivante: <br/>
  ![Capture du 2020-02-04 15-57-05](https://user-images.githubusercontent.com/22484369/73755912-0f2c8180-4767-11ea-915d-a115b1194a51.png)
- On réitère au début en gardant les nouvelles valeurs de phéromones sur les arrêtes


## License

- [MIT](LICENSE)

## Contributors

- Nicolas Martin
