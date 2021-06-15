import requests
import json
import pandas as pd
import os
import shutil

def sauvegarde_locale_stations(Npiezmin=10,Nech=20,Npage=1):
    """Sauivegarde en local toutes les infos correspondant à un échantillon de stations"""
    out=requests.get(f"https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/stations?format=json&page={Npage}&size={Nech}")
    stations=json.loads(out.text) # data est la donée json qui est affichée sur le site hubeau,  data['data'] est une liste, de dictionnaires correspondant aux données
    #stations est au format json
    data=pd.json_normalize(stations['data']) # j'extrais data, que je gere en table pandas
    data.loc[data['nb_mesures_piezo']>Npiezmin].to_csv('donnees/stations.csv')

def sauvegarde_locale_chroniques():
    """Met à jour les chroniques à partir de la base de données 'stations' """
    stations=pd.read_csv('donnees/stations.csv',index_col=0)
    try:
        shutil.rmtree('donnees/chroniques') # on vide le dossier chroniques
        print("Dossier donnees/chroniques enlevé")
    except :
        print("On ne peut pas enlever le dossier donnees/chroniques, peut être qu'il n'existe pas")
    try :
        os.mkdir('donnees/chroniques')
        print("Création d'un nouveau dossier donnees/chroniques")
    except :
        print("Pas de création du dossier donnees/chroniques, il existe peut être déja")
    indexes=stations.index.to_numpy()
    #stations.reset_index()
    #print(stations)
    for i in indexes:
        code_bss=stations.loc[i]['code_bss']
        out=requests.get(f"https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/chroniques?code_bss={code_bss}")
        chronique_json=json.loads(out.text)
        chronique=pd.json_normalize(chronique_json['data'])
        chronique.to_csv(f'donnees/chroniques/{i}.csv') #je les renomme avec les index qu'ils ont dans stations, car dans les code bss il y a des "/"
        
def sauvegarde_locale(Npiezmin=10,Nech=20,Npage=1):
    """Appelle les deux fonctions précédentes pour tout faire d'un coup, c'est elle qu'il faut appeller pour refaire completement la sauvegarde locale"""
    try :
        os.mkdir('donnees')
        print("Création d'un dossier donnees")
    except :
        print("Pas de création du dossier donnees, il existe peut être déja")
    sauvegarde_locale_stations(Npiezmin,Nech,Npage)
    sauvegarde_locale_chroniques()

def table_stations():
    """Renvoie la table stations stockée localement si elle existe (servira plus tard de base pour une fonction qui donne la base en regardant si elle existe localement ou pas)"""
    try :
        stations=pd.read_csv('donnees/stations.csv',index_col=0)
    except :
        print("pas de fichier stations.csv")
        return 0
    return stations

def extract_chronique_locale(code_bss):
    """Récupère une chronique à partir du code bss en recoupant à travers les différentes base de données"""
    stations=table_stations()
    if type(stations)=='int' : 
        return 0 # ca a déja affiché l'erreur
    try :
        index=stations[stations['code_bss']==code_bss].index.to_numpy()[0]
        chronique=pd.read_csv(f'donnees/chroniques/{index}.csv',index_col=0)
        return(chronique)
    except :
        print("Il n'y a un probleme pour trouver la chronique")
        return 0
    
def extract_chronique_remote(code_bss):
    """
    Extrait les niveaux pour la balise quicorrespond au code BSS fourni
    Renvoie un dataFrame pandas

    /!\ Pour récupérer plusieurs échantillons, faire les requêtes code bss par code bss, ne pas lui donner une liste de codes d'un coup
    """
    out=requests.get(f"https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/chroniques?code_bss={code_bss}")
    doneejson=json.loads(out.text)
    data=pd.json_normalize(doneejson['data'])
    return data

def extract_chronique(code_bss):
    """Cette fonction combine toutes les précédentes et lorsqu'on lui donne un code bss va d'abord chercher en local puis sur le serveur si la chronique voulue n'est pas en local."""
    try :
        chronique_locale=extract_chronique_locale(code_bss)
        chronique_locale['code_bss'] # l'idée est de générer une erreur si jamais on ne récupère pas un dataframe
        print(f"{code_bss} extracted from local storage")
        return chronique_locale
    except :
        print(f"{code_bss} extracted from server")
        return(extract_chronique_remote(code_bss))