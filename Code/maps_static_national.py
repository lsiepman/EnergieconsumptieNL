# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 15:41:24 2020

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
os.chdir("../Results/National_Map_Static")

#%% GAS plots (too slow in loop, more RAM necessary)
# i = 2008
# df = data.loc[(data["year"] == i) & (data["type"] == "gas")]
# df = fct.CorrectForConnection(df)
# df = fct.RemoveOutliers(df, "annual_consume_corrected")
# df = df.dropna(subset = ["LAT", "LON"])
# fsm.PlotStaticMap(df, "annual_consume_corrected", "Gas usage in the Netherlands {}".format(i), "Gas usage (m3)", shapes)
# del df

#%% ELECTRICITY PLOTS (too slow in loop, more RAM necessary)
i = 2015
df = data.loc[(data["year"] == i) & (data["type"] == "electricity")]
df = fct.CorrectForConnection(df)
df = fct.RemoveOutliers(df, "annual_consume_corrected")
df = df.dropna(subset = ["LAT", "LON"])
fsm.PlotStaticMap(df, "annual_consume_corrected", "Electricity usage in the Netherlands {}".format(i), "Electricity usage (kWh)", shapes)
del df
