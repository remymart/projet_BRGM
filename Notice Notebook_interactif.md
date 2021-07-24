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

# Guide d'utilisation de la bibliothèque "Notebook_interactif.py"


La bibliothèque contenue dans Notebook_interactif.py contient la fonction visualisation qui permet de représenter les données à étudier sur une carte.


# Les arguments de la fonction :

- stations : la table pandas des stations qui ont été tirée de la base et que l'on souhaite visualiser
- Nseuil : le nombre minimum de mesures qu'une station doit avoir pour être représentée.



# Les caractéristique de la carte :

   Les stations sont ensuites représentées sur une carte de la France par des points de couleur. Les stations aux couleurs les plus rouges sont celles qui ont le moins de mesures à leur actif, les plus vertes sont au contraire les stations avec de nombreuses mesures. L'échelle de couleur est propre aux stations séléctionnées initialement.
    
   Il est possible de zoomer et de se déplacer sur la carte. De plus, en passant la souris sur une station, le code BSS de celle-ci est affiché. Lorsque plusieurs stations se superposent on affiche les codes de toutes les stations sous la souris à la suite. Il est alors recommandé de zoomer pour plus de précision.

```python

```
