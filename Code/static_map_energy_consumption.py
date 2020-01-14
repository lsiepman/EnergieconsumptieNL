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


#%% PLOT
ax = plt.axes(projection=ccrs.PlateCarree())
plt.title('Nederland')
ax.add_geometries(shapes, ccrs.PlateCarree(),
                  edgecolor='black', facecolor='gray', alpha=0.2)
ax.set_extent([3, 8, 50.5, 54], ccrs.PlateCarree())

plt.show()