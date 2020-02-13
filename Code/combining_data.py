# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 10:22:48 2020

Combining data 
@author: laura
"""

#%% IMPORTS
import pandas as pd
import os
import functions_combine as fct

#%% SETTINGS
os.chdir("../Data")
pd.set_option('max_columns', 25)

#%% DATA
os.chdir("./Gas")
gas_files = os.listdir()
gas_data = fct.CombineFiles(gas_files)
gas_data["type"] = "gas"

os.chdir("../Electricity")
elec_files = os.listdir()
elec_data = fct.CombineFiles(elec_files)
elec_data["type"] = "electricity"

os.chdir("..")
geo_info = pd.read_csv("Geolocation.csv")

#%% COMBINE DATA GAS AND ELECTRICITY
data = pd.concat([gas_data, elec_data])

geo_data = pd.merge(data, geo_info, left_on = ["zipcode_from"], right_on = ["POSTCODE"], how = "left")

#%% EXPORT 
geo_data.to_csv("data_energy_geo.csv", index = False)
