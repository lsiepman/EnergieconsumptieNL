# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 11:57:08 2020

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
os.chdir("../Results")

#%% DATA PREP
data = data.loc[(data["year"] == 2018) & (data["type"] == "gas")]
data = f.CorrectForConnection(data)
data = f.RemoveOutliers(data, "annual_consume_corrected")
data = data.dropna(subset = ["LAT", "LON"])
data = data.groupby("city").mean()

#%% PLOT
f.PlotStaticMap(data, "annual_consume_corrected", "Average gas usage per city in the Netherlands (2018)", "Gas usage (m3)", shapes)

