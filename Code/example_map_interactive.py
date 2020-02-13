# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 09:11:35 2020
Interactive visualisation

@author: laura
"""
#%% IMPORTS
import pandas as pd
import os
import functions_general as fct
import functions_interactive_map as fim

#%% SETTINGS
os.chdir("../Data")
pd.set_option('max_columns', 25)

#%% DATA
data = pd.read_csv("data_energy_geo.csv")


#%% PREPARATION FOR MAPS
start_year = data["year"].min()
last_year = data["year"].max() + 1

gas = {}
for i in range(start_year, last_year):
    gas["gas{}".format(i)] = fim.InteractiveMapData(data, "gas", i)
    gas["gas{}".format(i)] = fct.RemoveOutliers(gas["gas{}".format(i)], "annual_consume_corrected")

elec = {} 
for i in range(start_year, last_year):
    elec["elec{}".format(i)] = fim.InteractiveMapData(data, "electricity", i)
    elec["elec{}".format(i)] = fct.RemoveOutliers(elec["elec{}".format(i)], "annual_consume_corrected")

#%% MAPS - more RAM needed for later years
os.chdir("../Results/National_Map_Interactive")
fim.PlotInteractiveMapYears(gas, "Gas", "annual_consume_corrected", "NL", "m3")
fim.PlotInteractiveMapYears(elec, "Electricity", "annual_consume_corrected", "NL", "kWh")


