# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 15:41:24 2020

@author: laura
"""

#%% IMPORTS
import functions as f
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

#%% PLOT PREP
years = list(range(2008, 2019))

#%% GAS plots (too slow in loop)
# i = 2008
# df = data.loc[(data["year"] == i) & (data["type"] == "gas")]
# df = f.CorrectForConnection(df)
# df = f.RemoveOutliers(df, "annual_consume_corrected")
# df = df.dropna(subset = ["LAT", "LON"])
# f.PlotStaticMap(df, "annual_consume_corrected", "Gas usage in the Netherlands {}".format(i), "Gas usage (m3)", shapes)
# del df

#%% ELECTRICITY PLOTS (too slow in loop)
i = 2015
df = data.loc[(data["year"] == i) & (data["type"] == "electricity")]
df = f.CorrectForConnection(df)
df = f.RemoveOutliers(df, "annual_consume_corrected")
df = df.dropna(subset = ["LAT", "LON"])
f.PlotStaticMap(df, "annual_consume_corrected", "Electricity usage in the Netherlands {}".format(i), "Electricity usage (kWh)", shapes)
del df
