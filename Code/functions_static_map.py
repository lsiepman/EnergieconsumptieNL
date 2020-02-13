# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:03:56 2020

@author: laura
"""

#%% IMPORTS
import cartopy.crs as ccrs
import branca.colormap as bcm
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm as cmx

#%%

def PlotStaticMap(data, col_usage, title, label_colorbar, shapes, extent = [3, 8, 50.5, 54]):
    """
    Plots a static map of energy usage in the Netherlands. The colour of the points indicates the usage.
    
    Parameters
    ------------
    data : pandas dataframe
        contains information about energy usage on specific locations. The longitude and latitude data should be in columns called 'LON' and 'LAT'.
    col_usage : str
        name of the column containing the usage data
    title : str
        title of the plot
    label_colorbar : str
        title of the color bar
    shapes : polygons
        a (list of) polygons that are used to draw the map
    extent : list of 4 int
        determines the zoom level and focus of the map. Has a default value that shows the entire country.     
    
    Returns
    --------
    Plot in the working directory
    
    """
    min_data = min(data[col_usage])
    max_data = max(data[col_usage])
    
    fig = plt.figure(figsize=(8, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_geometries(shapes, ccrs.PlateCarree(),
                  edgecolor='black', facecolor='gray', alpha=0.2)
    ax.set_extent(extent, ccrs.PlateCarree())
    norm = colors.Normalize(vmin = min_data, vmax = max_data)
    cmap = plt.get_cmap('RdYlGn_r') 
    m = cmx.ScalarMappable(cmap=cmap, norm = norm)

    for point in range(len(data[col_usage])):
        plt.plot(data["LON"].iloc[point], data["LAT"].iloc[point], 'o', color = m.to_rgba(data[col_usage].iloc[point]),transform=ccrs.PlateCarree())
    plt.title(title)
    cb = plt.colorbar(m)
    cb.set_label(label_colorbar)
    
    plt.savefig(title, dpi = 300)