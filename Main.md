---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.1
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
from spectre_freq import *
from Preprocess import *
from recuperation import *
from Notebook_interactif import *
from ipywidgets import interact, interact_manual, IntSlider, FloatSlider, Dropdown, fixed
from IPython.display import display
```

# Choix des stations à étudier :
Choisir les paramètres de recherche des stations qui seront retenues pour l'étude, puis appuyer sur Run Interact.

```python
interact_manual(sauvegarde_locale_stations, Nech = IntSlider(min=1,max=4000,value=100),Npiezmin=IntSlider(min=0,max=2000),Npage=IntSlider(min=1,max=5))
```

# Visualisation des stations :
La prochaine cellule permet de visualiser les différentes stations de mesure de france métropolitaine. Les stations en les plus rouges sont celles avec le moins de mesure. Il est possible d'appliquer un filtre pour n'observer que les stations avec beaucoup de mesures. On obtient le code BSS des stations en passant la souris dessus.

```python
table_stat = table_stations()
interact(visualisation, stations=fixed(table_stat), Nseuil = FloatSlider(min=0, max=2000, 
                                 step=10, value=10,
                                 continuous_update=False))
```

# Etude d'une chronique :
On écrit ensuite le code bss de la station que l'on souhaite étudier pour extraire la chronique associé.

```python
code_bss = '10396X0083/SA10'
stat=table_stat.loc[table_stat['code_bss']==code_bss]
print(stat.columns)
stat
```

```python
dataframe = extract_chronique(code_bss)
dataframe.head()
```

Preprocessing de la chronique de la station :

```python
dataframe = label_and_interpol_df(dataframe, tolerance = 7)

dataframe = filtre_valeur_aberrante(dataframe, normalize = True)

dataframe.head()
```

```python
newdf = regularize_timestep(dataframe, 'linear')
```

Analyse de la chronique :

```python
interact_manual(show_spectrum,
         table = fixed(newdf),
         filter = ['none','passe_bas'],
         f_coupure = FloatSlider(min=0,max=0.1, value=0.1, step=0.00001,readout_format='-5f')
        )
```

```python
df_modified=newdf.copy()
interact_manual(filtrage, table = fixed(df_modified), filter=fixed('passe_bas'),freq_coupure = FloatSlider(min=0,max=0.100,value=0.05,step=0.00001,readout_format='.5f')
)
```

```python
fig,ax=plt.subplots()
ax.plot(df_modified['date_mesure'],df_modified['niveau_nappe_eau'])
```
