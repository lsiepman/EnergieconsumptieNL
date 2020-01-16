# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 11:57:08 2020

@author: laura
"""
#%% IMPORTS
import functions as f
import pandas as pd
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
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


#%% PLOT PREP





#%% PLOT

plt.figure(figsize = (15, 15))
cmap = plt.cm.get_cmap("RdYlGn_r")
sm = plt.cm.ScalarMappable(cmap=cmap)
sm._A = []
cb = plt.colorbar(sm)
cb.set_ticks([])
ax = plt.axes(projection=ccrs.PlateCarree())
plt.title('Nederland')

ax.add_geometries(shapes, ccrs.PlateCarree(),
                  edgecolor='black', facecolor='gray', alpha=0.2)
ax.set_extent([3, 8, 50.5, 54], ccrs.PlateCarree())
plt.plot(data["LON"], data["LAT"], 'o', 
         transform=ccrs.PlateCarree())

plt.colorbar(sm)
plt.show()

#%% COLORBAR TESTING
from matplotlib import colorbar, colors, cm
import numpy as np

min_data = min(data.annual_consume_corrected)
max_data = max(data.annual_consume_corrected)

fig = plt.figure(figsize=(8, 5))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_geometries(shapes, ccrs.PlateCarree(),
                  edgecolor='black', facecolor='gray', alpha=0.2)
ax.set_extent([3, 8, 50.5, 54], ccrs.PlateCarree())
m = plt.cm.ScalarMappable(cmap=cm.RdYlGn_r)
m.set_clim(min_data, max_data)
plt.plot(data["LON"], data["LAT"], 'o',
         transform=ccrs.PlateCarree())
#cmap.set_array([])
plt.colorbar(m)

test = m.to_rgba(data["annual_consume_corrected"]) 

#%% LUKT HET OM 1 PUNT TE PLOTTEN
#https://stackoverflow.com/questions/43442925/color-coding-using-scalar-mappable-in-matplotlib
#https://stackoverflow.com/questions/8931268/using-colormaps-to-set-color-of-line-in-matplotlib
#https://stackoverflow.com/questions/15140072/how-to-map-number-to-color-using-matplotlibs-colormap
#https://stackoverflow.com/questions/43150687/colorbar-limits-are-not-respecting-set-vmin-vmax-in-plt-contourf-how-can-i-more
#PROBEER DE NORMALIZATION
#https://stackoverflow.com/questions/46027111/how-do-i-make-my-colour-bar-for-cartopy-have-a-specific-range-set-by-me