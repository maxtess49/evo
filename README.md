# Evolutionary Algorithm for M2 ID course: Algorithmes intelligents pour l’aide à la décision

## TODO:
### Selection functions
- [X] Tournament
- [X] Best
- [X] Random

### Crossover functions
- [X] Monopoint
- [X] Uniform

### Mutation functions
- [X] Bitflip
- [X] 1Flip
- [X] 3Flip
- [X] 5Flip

### Insertion functions
- [X] Fitness (Worst are discarded)
- [X] Age (Olders are discarded)

### Auto adjustment method
- [ ] Wheel
- [ ] Bandit
- [ ] Adaptative pursuit

### Random
- [X] Random seed
- [ ] Random seed choice

### Graf generator
- [ ] Add generator to main
- [ ] Add types of grafs (comparison of method frequency for wheel)

### Important
- [ ] Check for bias

### Test
- [ ] Add mutation operators to test


#### Notes

essayer d'avoir toujours du fitness positif (à voir ?)

Pour calculer l'efficacité d'une méthode, additionner les valeurs ajoutées au fitness, pas dans le négatif, prendre une fenêtre glissante (garder un historique) le problème de faire la full moyenne c'est que y'a une inertie quand un opérateur devient mauvais

La mutation est possible même sans croisement, mutation prise que si améliorant, attention, il faut cloner les listes en python pour pas modifier la liste d'origine
 
des op utilisés pour diversifier selon une formule

compter le nombre d'éval de fitness ou le nombre de flips testés (ou op testés)

toujours vérifier si y'a des biais (genre premier choix pour même utilité d'opérateur), c'est le plus important tout le temps

voir moodle et notebook pour "s'inspirer"

## How-To
Comming soon
