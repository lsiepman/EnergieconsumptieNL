# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:06:02 2020

@author: laura
"""

#%% IMPORTS
import pandas as pd
import os
from functions_general import CorrectForConnection, RemoveOutliers


#%% SETTINGS
os.chdir("../Data/CBS")
pd.set_option("max_columns", 25)

#%% DATA
age = pd.read_csv("Clean_CBS - Age (2008-2018).csv", dtype = {"ID" : int, "Perioden" : int, "Bevolking_1" : float})
imm = pd.read_csv("Clean_CBS - Household_composition (2008-2018).csv")
pos = pd.read_csv("Clean_CBS - Immigration (2008-2018).csv")
hou = pd.read_csv("Clean_CBS - Household_composition (2008-2018).csv")

os.chdir("..")
energy = pd.read_csv("data_energy_geo.csv")

#%% FUNCTIONS
def SplitYears(data, year_col):
    data = data.dropna(subset = [year_col])
    data[year_col] = data[year_col].astype(int)
    start_year = min(data[year_col])
    end_year = max(data[year_col]) + 1

    data_dict = {}
    for i in range(start_year, end_year):
        data_dict[i] = data.loc[data[year_col] == i]

    return data_dict
#%% DATA PREPARATION ENERGY
gas = energy.loc[energy["type"] == "gas"]
elec = energy.loc[energy["type"] == "electricity"]
del energy

gas = CorrectForConnection(gas)
gas.drop(["net_manager", "purchase_area", "street", "zipcode_from", "zipcode_to", "city", "type_conn_perc", "type_of_connection", "LON", "LAT"], axis = 1, inplace = True)
gas = RemoveOutliers(gas, "annual_consume_corrected")
gas["Postcode4"] = gas["POSTCODE"].str.extract("([0-9]+)")

gas_mean = gas.groupby(["Postcode4", "year"]).mean()
gas_median = gas.groupby(["Postcode4", "year"]).median()


#%% DATA PREPARATION CBS
age_years = SplitYears(age, "Perioden")
test = age_years[2008].pivot_table(index = ["Postcode"], columns = ["Geslacht", "Leeftijd"], values = "Bevolking_1")
