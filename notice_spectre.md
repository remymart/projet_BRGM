# Guide d'utilisation de la biliothèque "spectre_freq.py"

La bibliothèque définie dans le fichier "spectre_freq.py" permet d'implémenter quelques fonctions utiles d'analyse fréquentielle de Fourier et de filtrage fréquentiel.

## Régulariser les pas de temps d'une série
Dans le but de réaliser une analyse fréquentielle d'une série temporelle, il faut au préalable régulariser les pas de temps de la série, c'est-à-dire faire en sorte qu'il y ait un intervalle de temps constant entre deux mesures consécutives de la série. La fonction `regularize_timestep(table, filling_method)` permet de faire ce prétraitement, en faisant en sorte qu'il y ait une mesure par jour dans la série, en extrapolant les valeurs qui manquent dans la chronique tirée.  
Documentation :  
arguments :  
1. table: chronique sous la forme d'un tableau pandas
2. filling_method : méthode de remplissage à choisir parmi 3 méthodes:
a. 'zero_padding' (défaut) : ajoute des zéros aux jours non renseignés  
b. 'last_value': ajoute la dernière valeur renseignée dans la chronique aux jours non renseignés 
c. 'linear' : extrapole par une droite entre deux valeurs renseignées si il y a des jours non renseignés entre ces deux valeurs.    

renvoie : un dataframe panda ou on a rajouté des lignes qui correspondent aux mesures manquantes. 

  
  ## Observer le spectre fréquentielle d'une chronique :
  La bibliothèque permet de tracer le spectre fréquentiel d'une chronique avec la fonction `show_spectrum(table, filter , f_coupure)`.  
  Documentation :  
  permet de visualiser le spectre de Fourier de la chronique, en appliquant éventuellement un filtre  
arguments :  
1. table : dataframe panda qui correspond à la chronique récupérée après regularisation des pas de temps
2. filter : si égal à 'none' (par défaut), n'applique pas de filtrage. Si égal à 'passe_bas' applique un passe bas avec f_coupure comme fréquence de coupure
3. f_coupure : fréquence de coupure exprimée en jour-1 du passe-bas éventuellement appliqué. par défaut : 0.1
  
affiche : le spectre de Fourier de la chronique, éventuellement filtré

## Filtrer une série temporelle :
On peut également filtrer la série à l'aide d'un filtre passe-bas sans afficher le spectre, pour réaliser des traitements ultérieurs. On peut utiliser la fonction `filtrage(table, filter='passe_bas',freq_coupure)`.

Documentation : 

permet de filtrer la chronique temporelle. Attention, il faut que cette chronique ait un pas de temps régulier (voir la fonction regularize_timestep)  
arguments :
1. table : dataframe complet de la chronique
2. filter : type de filtre appliqué: (par défaut) 'passe_bas' 
3. freq_coupure : fréquence de coupure du filtre. par défaut égal à 0.1
  
renvoie : dataframe panda dont la colonne 'niveau_nappe_eau' a été filtré temporellement. 