# Guide d'utilisation de la biliothèque "recuperation.py"

*Rémy Martinez*

La bibliotèque contenue dans le fichier "recuperation.py" sert à récupérer des données depuis la base Hubeau du BRGM, en particulier les mesures puiézométriques de niveau de nappe phréatique. Elle permert de créer un échantillon de données stocké localement sur l'ordinateur.

Elle implémente différentes fonctions, chacune ayant une description détatillée fournie en tapant help([fonction]) dans un terminal.

### Liste des fonctions :

- sauvegarde_locale_stations(Npiezmin=10,Nech=20,Npage=1)
- sauvegarde_locale_chroniques()
- sauvegarde_locale(Npiezmin=10,Nech=20,Npage=1)
- table_stations()
- extract_chronique_locale(code_bss)
- extract_chronique_remote(code_bss)
- extract_chronique(code_bss)

### Arguments des fonctions :

- Npiezmin : seuil du nombre de mesures pour qu'une station soit enregistrée localement (pour ne garder que les stations avec un nombre de mesures supérieur à Npiezmin)
- Nech : Nombre d'échantillons à tirer de la base distante dans l'opération
- Npage : page de données à récupérer. Par exemple si on regle Nech=20 et Npage=1 on tire les données 0 à 20, avec Nech=20 Npage=2 on tire les données 20 à 40. Cela peut permettre d'avoir des nouvelles données si besoin.
- code_bss : chaine de caractère correspondant à l'ientifiant d'une station de la base Hubeau dont on veut récuperer les données.

## Pour utiliser cette bibliothèque on peut se baser sur le framework suivant : 

### Création d'un échantillon local :

Executer la fonction sauvegarde_locale(), elle va créer au niveau de la racine ou est executé python un dossier "donnees" contenant : 
- "stations.csv" qui correspond à la table stations de la base Hubeau
- un dossier "chroniques" qui correspond  au chroniques des stations de "stations.csv", stockées au format .csv , les nombres correspondent à l'indexation de la table "stations.csv". L'indexation de la base Hubeau par codes bss n' pas pu être réutilisée directement car les codes bss contiennent des caractères interdits dans les noms de fichiers (le "/" notamment). Cependant la correspondance est faite lorsuqu'on utilise les différentes fonctions pour que l'utilisateur ne voie pas de différence.

En théorie on n'a besoin d'executer cette fonction qu'une seule fois, car ensuite on a un échantillon stocké dans la mémoire de l'ordinateur (dit autrement on n'a pas besoin d'executer cette partie du code à chaque lacement de python mais eulement une fois pour toutes).

Dans le cas ou un fichier "donnees" existe déja : cette fonction le supprimme et crée un dossier comme mentionnée ci-dessus.

Cette partie tire des donnée depuis la base Hubeau distante, il faut donc disposer d'une connexion à unternet pour pouvoir l'executer correctement.

**Note :** sauvegarde_locale_chroniques() génère tout les contenu du dossier "chroniques" en tirant les données correspondant aux stations contenues dans stations.csv. Cela n'est pas utile en temps normal sauf dans le cas ou on veuille rafraîchir ou restaurer la partie "chroniques".

### Utilisation d'un échantillon précedement stocké :

Si on a précédemment créé et rempli le dossier "donnees", on peut ensuite exploiter notre échantillon comme ceci :

- table_stations() donne sous forme d'un dataFrame pandas l'échantillon de la table "stations" stocké sur la machine. Cet échantillon contient les mêmes champs que caux qu'il y a dans la base Hubeau.

- extract_chronique_locale(code_bss) et extract_chronique_remote(code_bss) permettent  partir du code BSS correspondant à une station d'aller en chercher la chronique respectivement sur l'échantillon stocké localement (avec un message d'erreur au cas ou il n'y ait pas cet échantillon dans la base locale) et sur la base distante. Elles erenvoient alors la chronique sous la forme d'un dataFrame pandas.

- extract_chronique(code_bss) combine les deux fonctione précédentes en allant chercher la chronique d'abord en local, puis sur la base distante en cas d'échec.



