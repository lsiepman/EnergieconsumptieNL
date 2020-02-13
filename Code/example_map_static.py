# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 11:57:08 2020

@author: laura
"""
#%% IMPORTS
import functions_general as fct
import functions_static_map as fsm
import pandas as pd
import cartopy.io.shapereader as shpreader
import os


#%% SETTINGS
os.chdir("../Data")
pd.set_option('max_columns', 25)

#%% DATA
shapes = list(shpreader.Reader("gadm36_NLD_shp/gadm36_NLD_1.shp").geometries())
data = pd.read_csv("data_energy_geo.csv")

#%% DATA PREP
data = data.loc[(data["year"] == 2008) & (data["type"] == "gas")]
data = fct.CorrectForConnection(data)
data = fct.RemoveOutliers(data, "annual_consume_corrected")
data = data.dropna(subset = ["LAT", "LON"])

#%% PLOT
os.chdir("../Results/National_Map_Static")

fsm.PlotStaticMap(data, "annual_consume_corrected", "Gas usage in the Netherlands (2008)", "Gas usage (m3)", shapes)

