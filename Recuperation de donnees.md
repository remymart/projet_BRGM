## L'idée de ceci est de faire un code qui permette d'extraire automatiquement les données du site

Ce notebook implémente 3 fonctions :
* Une qui va chercher els code bss des stations avec suffisament de mesures
* Une qui, pur un code bss donné, renvoie les mesuresde la stations
* Une troisième qui, pour un code bss donné, affiche la série temporelle des mesures

```python
import requests
import json
import pandas as pd
import numpy as np
```

## Je commence par faire quelques tests pour voir commet faire

```python
out=requests.get("https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/stations?format=json&page=1&size=20")
#out.headers['content-type']
stations=json.loads(out.text) # data est la donée json qui est affichée sur le site hubeau,  data['data'] est une liste, de dictionnaires correspondant aux données
#stations est au format json
data=pd.json_normalize(stations['data'])
# j'extrais data, que je gere en table pandas


data[['code_bss', 'date_debut_mesure', 'date_fin_mesure','nom_commune', 'x', 'y','geometry.coordinates', 'nb_mesures_piezo']] # j'ai selectionné des champs qui pouvaient être utiles

Npiezmin=10

data[['code_bss','nb_mesures_piezo','nom_commune']].loc[data['nb_mesures_piezo']>Npiezmin] # on récupère les code BSS des balises qui ont plus de Npiezmin mesures

```

```python
pd.json_normalize(json.loads(out.text))
```

```python
data.columns
```

## Maintenant on écrit des fonctions qui vont récupérer les données toutes seules

```python
def code_bss_piezmin(Npiezmin=10,Nech=20,Npage=1):
    """
    Extrait Nech valeurs de la base de données, celles correspondantes à la page Npage. Ensuite selection des code bss des stations avec plus de Npiezmin mesures.
    Renvoie un dataFrame pandas contenant des données utiles.
    """
    out=requests.get(f"https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/stations?format=json&page={Npage}&size={Nech}")
    stations=json.loads(out.text) # data est la donée json qui est affichée sur le site hubeau,  data['data'] est une liste, de dictionnaires correspondant aux données
    #stations est au format json
    data=pd.json_normalize(stations['data']) # j'extrais data, que je gere en table pandas
    return data[['code_bss','nb_mesures_piezo','nom_commune','code_departement','geometry.coordinates']].loc[data['nb_mesures_piezo']>Npiezmin] # on récupère les code BSS de
```

```python
code_bss_piezmin(Npiezmin=300,Nech=300)
```

```python
def extract_levels(code_bss):
    """
    Extrait les niveaux pour la balise quicorrespond au code BSS fourni
    Renvoie un dataFrame pandas

    /!\ Pour récupérer plusieurs échantillons, faire les requêtes code bss par code bss, ne pas lui donner une liste de codes d'un coup
    """
    out=requests.get(f"https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/chroniques?code_bss={code_bss}")
    doneejson=json.loads(out.text)
    data=pd.json_normalize(doneejson['data'])
    return data[['date_mesure','timestamp_mesure','niveau_nappe_eau','profondeur_nappe']]
```

```python
extract_levels("04454X0089/PK11.0") # j'ai entré une aderesse bss de dessus
```

### Note 
Pour avoir une table numpyu avec les valeurs du niveau piezo par ex : 

    Extraire les données des niveaux piezo : D=data["niveaux_piezo"]
    
    Le converir en numpy : D.to_numpy()

```python
levels=extract_levels("04454X0089/PK11.0")
levels['niveau_nappe_eau']
```


```python
niveaunp=levels['niveau_nappe_eau'].to_numpy()
profondeur=levels['profondeur_nappe'].to_numpy()
```

```python
datepd=pd.to_datetime(levels['date_mesure'])
dates=datepd.to_numpy()
dates[0]
```

```python
import matplotlib.pyplot as plt

plt.plot(dates,niveaunp)
plt.plot(dates,profondeur+225,color='y')
plt.plot(dates,profondeur+niveaunp,color='r',linestyle='--')
plt.grid()
plt.show()
```

Note : on voit que niveau nappe + profondeur = cte ... les deux données sont intimement liées

```python
# J'écris donc une fonction qui permet de visualiser la donnée (en compilant tout ce que j'ai écrit plus haut)
# il faut numpy, pandas, requests et matplotlib pour cette fonction

def show_level(code_bss):
    levels=extract_levels(code_bss)
    niveaunp=levels['niveau_nappe_eau'].to_numpy()

    datepd=pd.to_datetime(levels['date_mesure'])
    dates=datepd.to_numpy()

    plt.figure()
    plt.plot(dates,niveaunp)
    plt.title(f"Mesure {code_bss}")
    plt.grid()
    plt.xlabel("Temps")
    plt.ylabel("Niveau")
    plt.show()
```

```python
show_level("12288X0089/PIEZO.") # Balise a St Pierre, avec beaucoup de mesure et des valeurs abérrantes
# show_level("09892X0679/EXH70") # aussi beaucoup de valeurs

# show_level("08592X0175/FOR170") # étrange : celui ci ne marche pas

#show_level("00274X0010/F10")
```

```python
code_bss_piezmin(Npiezmin=0,Nech=10)["code_departement"][1]
```

#### Pour mettre tous les points sur une carte (je l'ai passé en markdown car assez long)


stations=code_bss_piezmin(Npiezmin=0,Nech=20000)
coordonee=stations['geometry.coordinates'].to_numpy()
coordonee=np.array(list(coordonee)) # sinon coordonnee est un array de listes

coordonee=coordonee[(coordonee[:,1]>-20)*(coordonee[:,0]<20)*(coordonee[:,1]<55)*(coordonee[:,1]>35),:]

plt.scatter(coordonee[:,0],coordonee[:,1])
plt.savefig("France")
plt.show()


### Tracé avec des couleurs en fonctin du nombre de mesures 

```python
Nseuil=2

coordoneebien=stations.loc[stations['nb_mesures_piezo']>Nseuil]['geometry.coordinates'].to_numpy()
coordoneebien=np.array(list(coordoneebien)) # sinon coordonnee est un array de listes
coordoneebien=coordoneebien[(coordoneebien[:,1]>-20)*(coordoneebien[:,0]<20)*(coordoneebien[:,1]<55)*(coordoneebien[:,1]>35),:]
plt.scatter(coordoneebien[:,0],coordoneebien[:,1],marker='+',color="g")

coordoneebof=stations.loc[stations['nb_mesures_piezo']<Nseuil]['geometry.coordinates'].to_numpy()
coordoneebof=np.array(list(coordoneebof)) # sinon coordonnee est un array de listes
coordoneebof=coordoneebof[(coordoneebof[:,1]>-20)*(coordoneebof[:,0]<20)*(coordoneebof[:,1]<55)*(coordoneebof[:,1]>35),:]
plt.scatter(coordoneebof[:,0],coordoneebof[:,1],marker="+",color="r")



plt.savefig("France_nombre")
plt.show()
```
