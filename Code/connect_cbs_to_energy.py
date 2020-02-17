# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:06:02 2020

@author: laura
"""

#%% IMPORTS
import pandas as pd
import os
from functions_general import CorrectForConnection, RemoveOutliers
import re

#%% SETTINGS
os.chdir("../Data/CBS")
pd.set_option("max_columns", 25)

#%% DATA
age = pd.read_csv("Clean_CBS - Age (2008-2018).csv")
imm = pd.read_csv("Clean_CBS - Household_composition (2008-2018).csv")
pos = pd.read_csv("Clean_CBS - Immigration (2008-2018).csv")
hou = pd.read_csv("Clean_CBS - Household_composition (2008-2018).csv")

os.chdir("..")
energy = pd.read_csv("data_energy_geo.csv")

#%% DATA PREPARATION
gas = energy.loc[energy["type"] == "gas"]
elec = energy.loc[energy["type"] == "electricity"]
del energy

gas = CorrectForConnection(gas)
gas = RemoveOutliers(gas, "annual_consume_corrected")
