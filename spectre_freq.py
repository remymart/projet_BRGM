import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    
#print(extract_levels("04454X0089/PK11.0"))# j'ai entré une aderesse bss de dessus 
table = extract_levels("04454X0089/PK11.0")
# print((table['date_mesure'][1]).split('-')[0])



def regularize_timestep(table, timestep = 'day', filling_method = 'zero_padding'):
	# trois timestep aux choix : jour, mois, année. Je sélectionne les valeurs, et en invente si il n'y a pas de données à un endroit.
	# seule l'option 'day' marche pour l'instant
	# la fonction renvoie deux array numpy qui correspondent aux timestamps régularisés et aux profondeurs correspondantes
	result_time = []
	result_depths = []
	
	if timestep == 'year':
		counter = 0
		while counter < len(table['date_mesure']) :
			year = int( (table['date_mesure'][counter]).split('-')[0] )
		
			year, depth, counter = average_year(table,counter,year)
			result_time.append(year)
			result_depths.append(depth)
			
			while int((table['date_mesure'][counter]).split('-')[0]) != (year + 1):
				year += 1
				result_time.append(year)
				result_depths.append(0)
		
		return result_time, result_depths
	if timestep == 'day':
		counter = 0 
		delta = 86400000 #nbre de ms dans un jour
		while counter < len(table['date_mesure']) - 1 :
			time = int( table['timestamp_mesure'][counter] )
			result_time.append(time)
			result_depths.append(table['niveau_nappe_eau'][counter])
			while int( table['timestamp_mesure'][counter+1]) != time + delta:
				result_time.append(time+delta)
				if filling_method == 'zero_padding':
					result_depths.append(0)
				if filling_method == 'last value':
					last_value = result_depths[-1]
					result_depths.append(last_value)
				time += delta
			counter += 1
		time_array = np.array(result_time)
		depth_array = np.array(result_depths)
		return time_array,depth_array
		

# def average_year(table,counter,year):
# 	mean_counter = 1
# 	S = table['niveau_nappe_eau'][counter]
# 	counter += 1
# 	while (table['date_mesure'][counter]).split('-')[0] == year:
# 		mean_counter += 1
# 		S += table['niveau_nappe_eau'][counter]
# 		counter += 1
# 	depth = (S/mean_counter)
# 	return year,depth,counter

# print(len(table['date_mesure']))
result, result1 = regularize_timestep(table,'day', 'last value')
# plt.scatter(result,result1)
# plt.show()

def show_spectrum(array_time, array_depth):
	array_spectrum = np.fft.fft(array_depth)
	array_freq = np.arange(len(array_time))
	plt.plot(array_freq,array_spectrum)
	plt.xlabel("fréquence en jour -1")
	plt.ylabel("amplitude")
	plt.show()

show_spectrum(result,result1)