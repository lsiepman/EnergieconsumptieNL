# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:42:49 2020

@author: laura
"""

#%% IMPORTS
import functions_general as fct
import functions_interactive_map as fim
import pandas as pd
import os
import re

#%% SETTINGS
os.chdir("../Data")
pd.set_option('max_columns', 25)

#%% DATA
data = pd.read_csv("data_energy_geo.csv")

#%% PLOT PREP
data["city"] = data["city"].str.replace("'S-GRAVENHAGE", "DENHAAG").str.replace("'S GRAVENHAGE", "DENHAAG")

cities = ["AMSTERDAM", "ROTTERDAM", "DENHAAG", "UTRECHT", "EINDHOVEN", "GRONINGEN", "TILBURG", "ALMERE", "BREDA", "NIJMEGEN"] #10 largest cities

start_year = data["year"].min()
last_year = data["year"].max() + 1

data = fct.CorrectForConnection(data)
data = data.dropna(subset = ["LAT", "LON"])

gas = {}
elec = {} 
for city in cities:
    df = data.loc[data["city"] == city]
       
    for i in range(start_year, last_year):
        gas["{0}_gas{1}".format(city, i)] = fim.InteractiveMapData(df, "gas", i)
        gas["{0}_gas{1}".format(city, i)] = fct.RemoveOutliers(gas["{0}_gas{1}".format(city, i)], "annual_consume_corrected")
    
    
    for i in range(start_year, last_year):
        elec["{0}_elec{1}".format(city, i)] = fim.InteractiveMapData(df, "electricity", i)
        elec["{0}_elec{1}".format(city, i)] = fct.RemoveOutliers(elec["{0}_elec{1}".format(city, i)], "annual_consume_corrected")
        
#%% PLOTS
os.chdir("../Results/Cities_Map_Interactive")        

for i in elec:
    if len(elec[i]) > 0:
        fim.PlotInteractiveMap(elec[i], i, "annual_consume_corrected", "Electricity usage in {0} [{1}] (kWh)".format(re.search(r"[A-Z]*", i).group(), re.search(r"[0-9]{4}$", i).group()))
    print("Finished", i)
    
for i in gas:
    if len(gas[i]) > 0:
        fim.PlotInteractiveMap(gas[i], i, "annual_consume_corrected", "Gas usage in {0} [{1}] (m3)".format(re.search(r"[A-Z]*", i).group(), re.search(r"[0-9]{4}$", i).group()))
    print("Finished", i)