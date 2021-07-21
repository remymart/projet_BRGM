import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
from recuperation import *
 


def string_date_to_date_date(string):
	""" la fonction convertit une date exprimée en format string sous la forme rencontrée dans les chronique en une date du module datetime de python
		arguments : date sous la forme décrite ci dessus (string)
		renvoie : la meme date sous le format datetime"""
	list = string.split('-')
	return date(int(list[0]),int(list[1]),int(list[2]))

def regularize_timestep(table,filling_method = 'linear'):
	"""la fonction régularise les pas de temps : elle parcourt jour par jour le tableau et ajoute une profondeur aux jours qui manquent
		arguments : 1)table: chronique sous la forme d'un tableau pandas
					2)filling_method : méthode de remplissage à choisir parmi 3 méthodes:
						a) 'zero_padding' (défaut) : ajoute des zéros aux jours non renseignés
						b) 'last_value': ajoute la dernière valeur renseignée dans la chronique aux jours non renseignés
						c) 'linear' : extrapole par une droite entre deux valeurs renseignées si il y a des jours non renseignés entre ces deux valeurs.
		renvoie : un dataframe panda ou on a rajouté des lignes qui correspondent aux mesures manquantes."""

	result_time = [] #en jours, comptés à partir de 0
	result_depths = []

	if filling_method == 'zero_padding' or filling_method == 'last_value':
		counter = 0 
		date_zero = string_date_to_date_date(table['date_mesure'][0])
		end = len(table['date_mesure']) - 1
		while counter < end :
			date_ = string_date_to_date_date(table['date_mesure'][counter])
			time = (date_ - date_zero).days
			diff = (string_date_to_date_date(table['date_mesure'][counter+1]) - date_).days
			while diff != 1:
				td = timedelta(time+1)
				result_time.append(date_zero + td)

				if filling_method == 'zero_padding':
					result_depths.append(0)
				if filling_method == 'last value':
					last_value = table['niveau_nappe_eau'][counter]
					result_depths.append(last_value)
				time += 1
				diff -=1
				
			counter += 1
		
		df = pd.DataFrame({'date_mesure': result_time , 'niveau_nappe_eau' : result_depths })
		table = table.append(df, ignore_index = True)
		table['date_mesure'] = pd.to_datetime(table.date_mesure)
		table.sort_values(by =['date_mesure'], inplace = True)
		
		return table
	
	if filling_method == 'linear':
		counter = 0
		date_zero = string_date_to_date_date(table['date_mesure'][0])
		temp_depth = []
		temp_time = []
		while counter < len(table['date_mesure']) - 1 :
			date_ = string_date_to_date_date(table['date_mesure'][counter])
			time = (date_ - date_zero).days
			# result_time.append(time)
			# result_depths.append(table['niveau_nappe_eau'][counter])
			diff = (string_date_to_date_date(table['date_mesure'][counter+1]) - date_).days
			if diff != 1:
				temp_depth=[]
				temp_time=[]
				
				h0 = float(table['niveau_nappe_eau'][counter])
				h1 = float(table['niveau_nappe_eau'][counter + 1])
				t0 = time
				t1 = (string_date_to_date_date(table['date_mesure'][counter+1]) - date_zero).days
				n = diff
				for i in range(1,n):
					temp_depth.append(((h1-h0)/n)*i + h0)
					td = timedelta(time+i)
					temp_time.append(date_zero + td)
				result_depths += temp_depth
				result_time += temp_time
			counter += 1
		# time_array = np.array(result_time)
		# depth_array = np.array(result_depths)
		df = pd.DataFrame({'date_mesure': result_time , 'niveau_nappe_eau' : result_depths })
		table = table.append(df, ignore_index = True)
		table['date_mesure'] = pd.to_datetime(table.date_mesure)
		table.sort_values(by =['date_mesure'], inplace = True)
		
		return table
			
				
def standardize(depth_array):
	""" centre et réduit les profondeurs pour avoir une meilleure vision en analyse fréquentielle
		argument : tableau array des profondeurs
		renvoie : le tableau array, mais la colonne des profondeurs est centrée réduite."""

	std = np.std(depth_array)
	mean = np.mean(depth_array)
	depth_array -= mean
	depth_array /= std
	return depth_array

def passe_bas(f_coupure,array_freq,array_spectrum):
	""" applique un filtre passe bas à un array fréquentiel, ie correspondant à la transformée de fourier d'un array issue d'une chronique de profondeurs
		le filtre met à zéro le tableau array_spectrum pour les fréquences supérieures à f_coupure.
		argument :  a)f_coupure : fréquence de coupure du filtre exprimée en jour-1
					b)array_freq : array numpy des fréquences
					c) array_spectrum : array numpy des modules de la transformée de fourier
		renvoie : l'array numpy array_spectrum auquel on a mis à zéro tous les coefficients qui correspondent à des fréquences plus hautes que f_coupure."""
	masque = (array_freq > f_coupure) | (array_freq < - f_coupure) 
	array_spectrum[masque] = 0 
	return array_spectrum

def show_spectrum(table, filter = 'none', f_coupure = 0.1):
	""" permet de visualiser le spectre de Fourier de la chronique, en appliquant éventuellement un filtre
		arguments : 1) table : dataframe panda qui correspond à la chronique récupérée après regularisation des pas de temps
					2) filter : si égal à 'none' (par défaut), n'applique pas de filtrage
								si égal à 'passe_bas' applique un passe bas avec f_coupure comme fréquence de coupure
					3) f_coupure : fréquence de coupure exprimée en jour-1 du passe-bas éventuellement appliqué. par défaut : 0.1
		affiche : le spectre de Fourier de la chronique, éventuellement filtré"""
	array_depth = np.array(table['niveau_nappe_eau'])
	array_depth = standardize(array_depth)
	array_spectrum = np.fft.fft(array_depth)
	array_freq = np.fft.fftfreq(array_spectrum.size)
	if filter == 'none':
		plt.plot(array_freq,np.abs(array_spectrum))
	if filter == 'passe_bas':
		array_spectrum = passe_bas(f_coupure,array_freq,array_spectrum)
		plt.plot(array_freq,np.abs(array_spectrum))
	plt.xlabel("fréquence en jour -1")
	plt.ylabel("amplitude")
	plt.show()
	return 1

def filtrage(table, filter='passe_bas',freq_coupure = 0.1) :
	""" permet de filtrer la chronique temporelle. Attention, il faut que cette chronique ait un pas de temps régulier (voir la fonction regularize_timestep)
		arguments : 1)table : dataframe complet de la chronique
					2)filter : type de filtre appliqué:
						(par défaut) 'passe_bas' 
					3)freq_coupure : fréquence de coupure du filtre. par défaut égal à 0.1
		renvoie : dataframe panda dont la colonne 'niveau_nappe_eau' a été filtré temporellement."""
	array_depth = np.array(table['niveau_nappe_eau'])
	if filter == 'passe_bas':
		array_depth = standardize(array_depth)
		array_spectrum = np.fft.fft(array_depth)
		array_freq = np.fft.fftfreq(array_spectrum.size)
		array_spectrum = passe_bas(freq_coupure,array_freq,array_spectrum)
		array_depth = np.fft.ifft(array_spectrum)
		table['niveau_nappe_eau'] = array_depth
	return table




