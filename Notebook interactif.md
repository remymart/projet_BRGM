---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
%matplotlib notebook
import matplotlib.pyplot as plt
import requests
import json
import pandas as pd
import numpy as np
from recuperation import *

```

```python
# les widgets pour construire le tableau de bord
from ipywidgets import interact, FloatSlider
from IPython.display import display
```

```python
sauvegarde_locale_stations(Nech=3000)
stations=pd.read_csv('donnees/stations.csv',index_col=0)
stations

```

```python
def filtre(Nseuil):   
    stations_retenues=stations.loc[(stations['nb_mesures_piezo']>Nseuil) & (stations['x']<50)& (stations['y']>30) ,:]

    coordoneebien=stations_retenues[['x','y']]
    x,y=coordoneebien.to_numpy()[:,0],coordoneebien.to_numpy()[:,1]
    names = stations_retenues['code_bss'].to_numpy()
    c = stations_retenues['nb_mesures_piezo'].to_numpy()
    max_c=max(c)
    cnorm = [int(255*float(i)/max_c) for i in c]

    norm = plt.Normalize(1,4)
    cmap = plt.cm.RdYlGn

    fig,ax = plt.subplots()
    sc = plt.scatter(x,y,c=cnorm, s=50, cmap=cmap, norm=norm)

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):

        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "{}".format(" ".join([names[n] for n in ind["ind"]]))
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor('w')
        annot.get_bbox_patch().set_alpha(0.4)


    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    plt.show()

```

```python
interact(filtre, Nseuil=FloatSlider(min=0, max=2000, 
                                 step=10, value=10,
                                 continuous_update=False))
```

```python

```
