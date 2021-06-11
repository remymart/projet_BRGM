import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
date_one = date(2020,3,2)
date_two = date(2020,3,3)

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
    
# print(extract_levels("04454X0089/PK11.0"))# j'ai entré une aderesse bss de dessus 
table = extract_levels("09433X0162%2FPIEZ")


def string_date_to_date_date(string):
	list = string.split('-')
	return date(int(list[0]),int(list[1]),int(list[2]))

def regularize_timestep(table,filling_method = 'zero_padding'):
	# Je sélectionne les valeurs, et en invente si il n'y a pas de données à un endroit.
	# méthodes de remplissage : 'zero_padding', 'last_value', 'linear'
	# la fonction renvoie deux array numpy qui correspondent aux timestamps régularisés et aux profondeurs correspondantes
	result_time = [] #en jours, comptés à partir de 0
	result_depths = []

	if filling_method == 'zero_padding' or filling_method == 'last_value':
		counter = 0 
		#delta = 86400000 #nbre de ms dans un jour
		date_zero = string_date_to_date_date(table['date_mesure'][0])
		
		while counter < len(table['date_mesure']) - 1 :
			date_ = string_date_to_date_date(table['date_mesure'][counter])
			time = (date_ - date_zero).days
			result_time.append(time)
			result_depths.append(table['niveau_nappe_eau'][counter])
			diff = (string_date_to_date_date(table['date_mesure'][counter+1]) - date_).days
			while diff != 1:
				result_time.append(time+1)
				if filling_method == 'zero_padding':
					result_depths.append(0)
				if filling_method == 'last value':
					last_value = result_depths[-1]
					result_depths.append(last_value)
				time += 1
				diff -=1
				
			counter += 1
		time_array = np.array(result_time)
		depth_array = np.array(result_depths)
		return time_array,depth_array
	
	if filling_method == 'linear':
		counter = 0
		# delta = 86400000
		date_zero = string_date_to_date_date(table['date_mesure'][0])
		temp_depth = []
		temp_time = []
		while counter < len(table['date_mesure']) - 1 :
			date_ = string_date_to_date_date(table['date_mesure'][counter])
			time = (date_ - date_zero).days
			result_time.append(time)
			result_depths.append(table['niveau_nappe_eau'][counter])
			diff = (string_date_to_date_date(table['date_mesure'][counter+1]) - date_).days
			if diff != 1:
				temp_depth=[]
				temp_time=[]
				
				h0 = table['niveau_nappe_eau'][counter]
				h1 = table['niveau_nappe_eau'][counter + 1]
				t0 = time
				t1 = (string_date_to_date_date(table['date_mesure'][counter+1]) - date_zero).days
				n = diff
				for i in range(1,n):
					temp_depth.append(((h1-h0)/n)*i + h0)
					temp_time.append(t0 + i)
				result_depths += temp_depth
				result_time += temp_time
			counter += 1
		time_array = np.array(result_time)
		depth_array = np.array(result_depths)
		return time_array,depth_array
			
				
def standardize(depth_array):
	#renvoie la série de depth_array centrée-réduite pour avoir une meilleure vision fréquentielle. Essentiel pour l'analyse fréquentielle, sinon le pic de valeur moyenn
	#écrase les pics de variation variationnelle.
	std = np.std(depth_array)
	mean = np.mean(depth_array)
	depth_array -= mean
	depth_array /= std
	return depth_array
					
				
result, result1 = regularize_timestep(table,'linear')
# plt.plot(result,standardize(result1))
# plt.show()

def passe_bas(f_coupure,array_freq,array_spectrum):
	masque = (array_freq > f_coupure) | (array_freq < - f_coupure) 
	array_spectrum[masque] = 0 
	return array_spectrum

def show_spectrum(array_time, array_depth, filter = 'none'):
	array_depth = standardize(array_depth)
	array_spectrum = np.fft.fft(array_depth)
	array_freq = np.fft.fftfreq(array_spectrum.size)
	if filter == 'none':
		plt.plot(array_freq,np.abs(array_spectrum))
	if filter == 'passe_bas':
		array_spectrum = passe_bas(0.1,array_freq,array_spectrum)
		plt.plot(array_freq,np.abs(array_spectrum))
	plt.xlabel("fréquence en jour -1")
	plt.ylabel("amplitude")
	plt.show()
	return 1

#show_spectrum(result,result1, 'passe_bas')

def filtrage(array_depth, filter='passe_bas',freq_coupure = 0.05) :
	if filter == 'passe_bas':
		array_depth = standardize(array_depth)
		array_spectrum = np.fft.fft(array_depth)
		array_freq = np.fft.fftfreq(array_spectrum.size)
		array_spectrum = passe_bas(freq_coupure,array_freq,array_spectrum)
		array_depth = np.fft.ifft(array_spectrum)
	return array_depth

plt.plot(result,filtrage(result1))
plt.show()

		




