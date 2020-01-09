# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 10:22:48 2020

Verkennen data 
@author: laura
"""

#%% IMPORTS
import pandas as pd
import os
import re

#%% SETTINGS
os.chdir("../Data")
pd.set_option('max_columns', 25)

#%% FUNCTIONS
def CombineFiles(list_of_files):
    """ Combines different csv files from the same working directory. Corrects for shifted year labels.
        
    Parameters
    -----------
    list_of_files : list of csv files from working directory that have to be combined 
    
    Returns
    ----------
    dataframe
    """
    data = []
    for file in list_of_files:
        df = pd.read_csv(file)
        name = file.replace(".csv", "")
        year = re.search(r"[0-9]{4}$", name).group()
        year_corrected = int(year) - 1 #correct for the year shift
        df["year"] = year_corrected
        data.append(df)
        
    data = pd.concat(data, sort = False)    
         
    return data

#%% DATA
os.chdir("./Gas")
gas_files = os.listdir()
gas_data = CombineFiles(gas_files)
gas_data["type"] = "gas"

os.chdir("../Electricity")
elec_files = os.listdir()
elec_data = CombineFiles(elec_files)
elec_data["type"] = "electricity"

os.chdir("..")
geo_info = pd.read_csv("Geolocation.csv")

#%% COMBINE DATA
data = pd.concat([gas_data, elec_data])

geo_data = pd.merge(data, geo_info, left_on = ["zipcode_from"], right_on = ["POSTCODE"], how = "left")

#%% EXPORT
geo_data.to_csv("data_energy_geo.csv", index = False)
