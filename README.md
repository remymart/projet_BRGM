# projet_BRGM


# Données piézométriques
## Contexte
    Il existe environ 20k stations de mesures (puits/forages) en France du niveau piézométriques (niveau d'eau dans le sous sol).
    La liste des stations est accessible via l'api hubeau :
    https://hubeau.eaufrance.fr/page/api-piezometrie
    et son opérateur "stations"
    https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/stations?format=json&size=20

    Pour chaque station, des données sont associées, et sont accessibles grâce à l'opérateur 'chroniques'
    https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/chroniques?code_bss=07548X0009%2FF&size=20

## Problématique
    1- Ces données sont des données 'de capteur' c'est à dire enregistrées sur le terrain. Elles souffrent donc de différents problèmes : lacune, dérive de capteur, changemnet de pas de temps d'acquisition, changement de résolution du matériel, changement du repère de mesure etc.
    Une partie de ces problèmes est corrigée lors que la mise en base de données, mais certaines erreurs (souvent historiques) persistent. Un enjeu est donc de les identifier, puis d'adopter une stratégie pour les gérer.
    Le projet pourrait se focaliser sur cet aspect : il s'agit alors de proposer des méthodes pour identifier / discriminer le signal 'vrai' du signal total. Différentes méthodes sont envisageables : en utilisant des méthodes issues du traitement du signal (acoustique, électrique), des méthodes statistiques, voire des approches 'intelligentes' (IA), via du clustering par exemple (random forest permet de faire une partie du travail).
   
    2- Une fois débarassé de ces différents écueils, le signal exprimé au niveau de la station de mesure n'est pas forcément simple à interpréter, car différents signaux s'expriment : le signal climatique (pluie principalement), le signal anthropique (pompage dans l'aquifère, modification dans la zone d'alimentation (imperméabilisation des sols, changement d'occupation du sol,...)) et ces signaux peuvent avoir des structures très différentes : impact très ponctuel (pompage), ou à grande longeur d'onde (pluie/cycle d'années humides/sècges).
    Au niveau d'une station, un travail possible est donc d'imaginer et concevoir des outils pour mettre en évidence les composantes du signal : stationnarité/non-stationnarité, autocorrélation, tendance, patterns, etc.
   
    3- Enfin, une approche complémentaire peut être de considérer non plus la station seule, mais un ensemble de station. Cela revient à considérer que l'on observe un même objet (un aquifère) à plusieurs endroits. On peut alors se poser la question de la propagation d'un signal (l'effet de la pluie par exemple) dans cet aquifère, et travailler sur la propagation, la distortion du signal.
   
    Rendu ?
    30 juin : forum
   
## Comment évaleur la réussite du projet ?
La réussite du projet peut être évaluer sur différents plans (sans ordre de préférence) :
    * capacité à produire un utilitaire pour accéder aux données (fonction, classe, exécutable, notebook,...)
    * capacité à exposer les données (cartes, graphiques, descripteurs statistiques)
    * capacité à exposer les méthodes de détections d'anomalies, de les documenter, de proposer des solutions de contournement, de correction,...
    * capacité à exposer des méthodes d'analyse du signal
    * originalité des solutions/approches, robustesses, passage à l'échelle possible, capacité à être automatisé, etc.
   
 ## Suivi de projet :
    * pour une prochaine réunion : proposition de faire une sorte de rapport d'étonnement : facilité/difficulté à prendre en charge en charge les api's, faire qq graphs, des stats, des cartes, regarder un signal sur quelques stations, etc. sont des approches possibles.
