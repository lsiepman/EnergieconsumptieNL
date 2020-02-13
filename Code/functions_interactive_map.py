# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 13:06:45 2020

@author: laura
"""

#%% IMPORTS
import pandas as pd
from functions_general import CorrectForConnection
import folium
import branca.colormap as bcm
import matplotlib.pyplot as plt
from matplotlib import colors
import re

#%% FUNCTIONS
def InteractiveMapData(data, energy_type, year):
    """Selects the data for the interactive map. Removes rows with 0 active connections and corrects for the number of active connections per zipcode.
    
    Parameters
    -----------
    data : pandas dataframe
        energy consumption data
    energy_type : str 
        "gas", or "electricity"
    year  : int 
        year to plot
    
    Returns
    -----------
    subset of original dataframe
    """
    df = data.loc[(data["type"] == energy_type) & (data["year"] == year)]
    df = df.dropna(subset = ["LAT", "LON"]).reset_index(drop = True) #data without geolocations are removed
    df = CorrectForConnection(df) #correct for number of active connections
    df = df.loc[df["perc_of_active_connections"]!= 0] #remove inactive connections with energy consumption 
    
    return df


def PlotInteractiveMap (data, filename, usage_col, caption_legend):
    """Creates a folium map (JS Leaflet) and saves it in the current working directory
    
    Parameters
    --------------
    data : pandas dataframe 
        subset of the energy consumption data
    filename : str 
        final filename, without file extension
    usage_col : str 
        name of column of energy usage
    caption_legend : str 
        title of the legend
        
    Returns
    -----------
    HTML file with interactive map

    """
    #color scale
    cmap = bcm.LinearColormap(['green', 'yellow', 'red'], vmin=data[usage_col].min(), vmax=data[usage_col].max())
    cmap.caption = caption_legend
    
    #create map
    interactive_map = folium.Map(location = [52.092876, 5.104480], zoom_start = 6.5)
    interactive_map.add_child(cmap)

    #plot points
    for i in range(len(data)):
        folium.CircleMarker(location = [data["LAT"].iloc[i], data["LON"].iloc[i]], 
                        radius = 2, weight = 0, fill_opacity = 1, fill = True, fill_color = cmap(data[usage_col].iloc[i])).add_to(interactive_map)

    #save map
    interactive_map.save("{}.html".format(filename))
    
    
def PlotInteractiveMapYears(energy_dict, type_energy, data_col, filename_base, unit_energy):
    """Uses the PlotInteractiveMap function to plot a series of interactive maps
    
    Parameters
    -----------
    energy_dict : dictionary of dataframes
        dictionary containing dataframes for each year you want to plot on a map
    type_energy : str
        type of the energy stored in the dictionary, used in legend caption
    data_col : str
        name of the column containing the data
    filename_base : str
        standard section of all filenames, without file extension
    unit_energy : str
        unit of the energy type, used in legend caption
        
    Returns
    -----------
    saves the html folium maps in the current working directory
    """
    for i in energy_dict:
        PlotInteractiveMap(energy_dict[i], "{0}_{1}".format(filename_base, i), data_col, "{0} consumption in {1} ({2})".format(type_energy, re.search(r"[0-9]{4}$", i).group(), unit_energy)) 
        print("finished {}".format(i))