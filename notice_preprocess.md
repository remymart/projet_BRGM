# Guide d'utilisation du fichier "preprocess.py"

Le fichier "preprocess.py" premet de préparer un minimum les données pour pouvoir les utiliser par la suite.
En effet, la base de données que l'on recoit est créée à partir de mesures ponctuelles de la hauteur de la nappe pour chque station, il existe donc parfosi des périodes de durées arbitrairement longues sans mesure. Or, pour analyser un signal et des données, il y a certaines conventions à respecter pour permettre une bonne analyse. Cette partie a pour but de préprarer ("préprocesser") les données que l'on recoit de cettte base de données.


## Trouver et combler les trous de données


La première fonction étbalit une labelisation des données que l'on recoit. On a en entrée un dataframe que l'on a prélevé sur la base de données (extrait grâce au code BSS). Le dataframe contient un ombre conséquent d'informations que l'on ne souhaite pas particulièrement utiliser, on va donc en garder que certaines : le code BSS, le niveau d'eau, les timestamp, les dates et une dernière colonne, la labelisation, que l'on crée donc avec cette première fonction.



La fonction `find_holes` prend en argument une dataframe et renvoie le signal avec les trous comblés par une interpolation linéaire.  
La labelisation associée est :   
0 si il s'agit d'une valeur initiale ;   
1 si la valeur est rajoutée par interpolation et si la duree sans nouvelle valeur est jugée courte -inferieur à 2 fois 'tolerance'- ;   
2 si la valeur est rajoutée par interpolation et si la durée est jugée longue (supérieure égale à 2 fois 'tolérance')  

L'interpolation créée est linéaire dans premier temps, ce qui peut être changé car le phénomène physique ne l'est pas.  
Cette fonction renvoie en sortie trois listes, contenant les nouveaux niveaux d'eaux (une addition de ceux crées et de ceux déja existant), les nouveaux timestamp et la labelisation associée à ces points.



C'est la fonction suivante, `label_and_interpol_df` qui fait le travail demandé.
Elle permet juste de prendre en argument un dataframe de la base de données enregistré en local et de créer en sortie un nouveau dataframe qui contient les 5 colonnes citées au dessus, réajusté.


## Normalisation des données


la fonction `filtre_ecart_type_and_normalize` prend en entrée un dataframe et renvoie en sortie une liste des niveaux corrigés : le but et d'enlever les valeurs abberrantes (en filtrant les valeurs jugées trop loin de la moyenne par raport à l'ecart type) et de remplacer les valeurs modifiées par une interpolation linéaire des valeurs aux alentours. On normalise ensuite le signal en soustrayant par la moyenne et en divisant par l'écart-type (process normal dans une procedure de traitement de données).


La fonction `filtre_valeur_aberrante` produit la même chose que la focntion précédente, à l'exeption qu'elle renvoie en sortie à nouveau un dataframe au format souhaité.
