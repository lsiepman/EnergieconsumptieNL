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

#%% FUNCTIES
def CombineFiles(list_of_files):
    """ Combineert verschillende csv bestanden uit dezelfde map. 
    Corrigeert ook voor de verkeerde nummering van de jaren.
    
    Parameters
    -----------
    list_of_files : lijst met csv-bestandsnamen uit de huidige working directory die moeten worden gecombineerd 
    
    Returns
    ----------
    dataframe
    """
    data = []
    for file in list_of_files:
        df = pd.read_csv(file)
        name = file.replace(".csv", "")
        year = re.search(r"[0-9]{4}$", name).group()
        year_corrected = int(year) - 1 #hier corrigeer ik voor het jaartal
        df["jaar"] = year_corrected
        data.append(df)
        
    data = pd.concat(data, sort = False)    
         
    return data

#%% DATA
os.chdir("./Gas")
gas_files = os.listdir()
gas_data = CombineFiles(gas_files)
gas_data["Soort"] = "gas"

os.chdir("../Electricity")
elec_files = os.listdir()
elec_data = CombineFiles(elec_files)
elec_data["Soort"] = "electricity"



os.chdir("..")
geo_info = pd.read_csv("Adressen en coordinaten NL.csv")
geo_info.drop(["NUMBER", "STREET", "UNIT", "DISTRICT", "REGION", "ID", "HASH", "CITY"], axis = 1, inplace = True)
geo_info.drop_duplicates(subset = ["POSTCODE"], inplace = True)

#%% COMBINEREN DATA
data = pd.concat([gas_data, elec_data])

geo_data = pd.merge(data, geo_info, left_on = ["zipcode_from"], right_on = ["POSTCODE"], how = "left")

#%% EXPORT
geo_data.to_csv("data_energie_geo.csv", index = False)
