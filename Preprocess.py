import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from recuperation import *
################################################################################################################################################################

##1ere partie : ici le but est de combler les trous de données (pour faire en sorte qu'il n'y en ai pas de plus d'une semaine), puis de labesliser les données
## en fonction de si ces données sont créées, aberrantes ou d'origine.

def find_holes(df, tolerance = 7):
    """Cette fonction prend en argument une dataframe et renvoie le signal avec les trous comblés par une interpolation linéaire.
    La labelisation associée est : 
    0 si il s'agit d'une valeur initiale ; 
    1 si la valeur est rajoutée par interpolation et si la duree sans nouvelle valeur est jugée courte -inferieur à 2 fois 'tolerance'- ; 
    2 si la valeur est rajoutée par interpolation et si la durée ets jugée longue """
    
    levels = df['niveau_nappe_eau'].to_numpy().copy()
    dates = df['date_mesure'].to_numpy().copy()
    date_ts = df['timestamp_mesure'].to_numpy().copy()
    N = len(date_ts)
    
    new_levels = []
    new_dates_ts = []
    labelisation = []
    
    for i, date in enumerate(date_ts):
        if i<N-1:
            
            duree = date_ts[i+1] - date_ts[i]
            tol_nb_day = tolerance*24*3600*1000 # ce nombre de timestamp correspond à 1 semaine de base
            
            if duree > tol_nb_day :
                new_dates_ts.append(date)
                new_levels.append(level[i])
                labelisation.append(0)
                
                for j in range(duree//tol_nb_day):
                    new_date = date + (j+1)*tol_nb_day
                    new_level = level[i] + ((j+1)*tol_nb_day/duree)*(level[i+1]-level[i])
                    if duree//tol_nb_day == 1:
                        label = 1
                    elif duree//tol_nb_day > 1:
                        label = 2
                    
                    new_levels.append(new_level)
                    new_dates_ts.append(new_date)
                    labelisation.append(label)
            
            else :
                new_date = date
                new_level = levels[i]
                label = 0
                new_levels.append(new_level)
                new_dates_ts.append(new_date)
                labelisation.append(label)
    
    
    return(new_dates_ts, new_levels, labelisation)



def timestamp_to_date(liste):
    """Convertie une liste de timestamp en datetime"""
    new_liste = []
    for element in liste:
        new_element = pd.to_datetime(element)
        new_liste.append(new_element)
    return(new_liste)    



def label_and_interpol_df(df, tolerance = 7):
    """Cette fonction prend en argument une dataframe et renvoie un nouveau dataframe avec les trous comblés par une interpolation linéaire, ainsi qu'une labelisation des données.
    Le nouveau df possède 5 colonnes qui sont dans l'ordre : code_bss ; niveau_nappe_eau (qui a été corrigé ici) ; date_mesure ; timestamp_mesure ; label_new_value.  
    La labelisation associée est : 
        0 si il s'agit d'une valeur initiale ; 
        1 si la valeur est rajoutée par interpolation et si la duree sans nouvelle valeur est jugée courte -inferieur à 2 fois 'tolerance'- ; 
        2 si la valeur est rajoutée par interpolation et si la durée ets jugée longue """
    
    new_dates_ts, new_levels, labelisation = find_holes(df, tolerance)
    new_dates = timestamp_to_date(new_dates_ts)
    code_bss = df['code_bss'].to_numpy().copy()
    code = code_bss[0]
    
    new_df = pd.DataFrame(columns=['code_bss','niveau_nappe_eau', 'date_mesure', 'timestamp_mesure', 'label_new_value'])
    
    N = len (new_dates_ts)
    
    for i, new_level in enumerate(new_levels):
        new_date_ts = new_dates_ts[i]
        new_date = new_dates[i]
        label = labelisation[i]
        new_row = pd.DataFrame(data = np.array([[code, new_level, new_date, new_date_ts, label]]), columns = ['code_bss', 'niveau_nappe_eau', 'date_mesure', 'timestamp_mesure', 'label_new_value'])
        new_df = pd.concat([new_df, new_row], ignore_index=True)
    
    return(new_df)


#C'est la dernière fonction ci-dessus qu'il faut utiliser pour créer les valeurs necessaires. 
#Cette fonction renvoie un nouveau dataframe avec les valeurs corrigées et labelisées. 
#Il y a precisement 5 colonnes, avec dans l'ordre :
#   1ere colonne : le code_ss de la station (identique dans tout le df)
#   2eme colonne : le niveau_nappe_eau qui a été modifié
#   3eme colonne : le date_mesure avec les dates de mesure (ou celles qui ont été créées)
#   4eme colonne : le timestamp_mesure avec la meme chose que date_mesure masi avec des timestamp
#   5eme colonne : le label_new_value avec la labelisation des données : 0 si c'est une vraie valeur, 
                                                                        #1 si elle a été créée mais est exploitable par la suite,
                                                                        #2 si elle a été créée mais est totalement inexploitable, juste pour remplir un trou


################################################################################################################################################################
def mean_std_df(df):
    """Cette fonction permet à partir d'un dataframe labelisé de calculer moyenne et écart-type mais 
    uniquement sur les valeurs qui ne sont pas labelisé par 2, cad jugée pertinantes """
    
    niveau = df['niveau_nappe_eau'].to_numpy().copy()
    labelisation = df['label_new_value'].to_numpy().copy()
    
    list_without_created_values = []
    for i, level in enumerate(niveau):
        if labelisation[i] != 2 :
            list_without_created_values.append(level)
    final_list = np.array(list_without_created_values)
    return(np.mean(final_list), np.std(final_list))


def filtre_ecart_type_and_normalize(df, normalize = True):
    """Cette fonction filtre les signaux dont certaines valeurs rares sont abusivement aberante donc supprimée car trop loin de la moyenne. 
    On peut aussi en option normaliser le signal"""

    niveau = df['niveau_nappe_eau'].to_numpy().copy()
    dates = pd.to_datetime(df['date_mesure']).to_numpy().copy()
    labelisation = df['label_new_value'].to_numpy().copy()
    
    N = len(niveau)
    
    mean, std = mean_std_df(df)
    for i, prof in enumerate(niveau):
        if abs(prof - mean) > 4*std and labelisation !=2:
            if i != 0 and i != N:
                niveau[i] = (niveau[i-1] + niveau[i+1])/2
                
            if i == 0:
                niveau[i] = niveau[i+1]
                
            if i == N:
                niveau[i] = niveau[i-1]
    
    niveau = np.array(niveau)
    
    if normalize == True :
        new_mean = np.mean(niveau)
        new_std = np.std(niveau)
        niveau = (niveau - mean)/std
    return(niveau)


def filtre_valeur_aberrante(df):
    """Cette fonction filtre les signaux dont certaines valeurs rares sont abusivement aberante donc supprimée car trop loin de la moyenne. 
    Cette fonction renvoie un dataframe avec 5 colonnes dans l'ordre : code_bss ; niveau_nappe_eau (qui a été corrigé et normalisé) ; date_mesure ; timestamp_mesure ; label_new_value.
    On peut aussi en option normaliser le signal"""
    dates_ts = df['timestamp_mesure'].to_numpy().copy()
    dates = pd.to_datetime(df['date_mesure']).to_numpy().copy()
    labelisation = df['label_new_value'].to_numpy().copy()
    code_bss = df['code_bss'].to_numpy().copy()
    code = code_bss[0]
    new_levels = filtre_ecart_type_and_normalize(df)
    
    new_df = pd.DataFrame(columns=['code_bss','niveau_nappe_eau', 'date_mesure', 'timestamp_mesure', 'label_new_value'])

    for i, new_level in enumerate(new_levels):
        new_date_ts = dates_ts[i]
        new_date = dates[i]
        label = labelisation[i]
        new_row = pd.DataFrame(data = np.array([[code, new_level, new_date, new_date_ts, label]]), columns = ['code_bss', 'niveau_nappe_eau', 'date_mesure', 'timestamp_mesure', 'label_new_value'])
        new_df = pd.concat([new_df, new_row], ignore_index=True)
    
    return(new_df)