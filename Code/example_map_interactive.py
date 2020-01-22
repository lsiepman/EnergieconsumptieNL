# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 09:11:35 2020
Visualisatie op de kaart

@author: laura
"""
#%% IMPORTS
import pandas as pd
import os
import functions as f

#%% SETTINGS
os.chdir("../Data")
pd.set_option('max_columns', 25)

#%% DATA
data = pd.read_csv("data_energy_geo.csv")
os.chdir("../Results/National_Map_Interactive")

#%% PREPARATION FOR MAPS
start_year = data["year"].min()
last_year = data["year"].max() + 1

data = data.loc[data["city"] == "AMSTERDAM"]

gas = {}
for i in range(start_year, last_year):
    gas["gas{}".format(i)] = f.MapData(data, "gas", i)
    gas["gas{}".format(i)] = f.RemoveOutliers(gas["gas{}".format(i)], "annual_consume_corrected")

elec = {} 
for i in range(start_year, last_year):
    elec["elec{}".format(i)] = f.MapData(data, "electricity", i)
    elec["elec{}".format(i)] = f.RemoveOutliers(elec["elec{}".format(i)], "annual_consume_corrected")

#%% MAPS [can be slow]
f.PlotInteractiveMapYears(gas, "Gas", "annual_consume_corrected", "Amsterdam", "m3")
f.PlotInteractiveMapYears(elec, "Electricity", "annual_consume_corrected", "Amsterdam", "kWh")


#
#
