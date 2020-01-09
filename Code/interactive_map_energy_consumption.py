# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 09:11:35 2020
Visualisatie op de kaart

@author: laura
"""
#%% IMPORTS
import pandas as pd
import folium
import os
import branca.colormap as cm
import re


#%% SETTINGS
os.chdir("../Data")
pd.set_option('max_columns', 25)

#%% FUNCTIONS
def MapData(data, energy_type, year):
    """Selects the data for the map. Removes rows with 0 active connections and corrects for the number of active connections per zipcode.
    
    Parameters
    -----------
    data : dataframe
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
    df["annual_consume_corrected"] = df["annual_consume"]/(df["num_connections"]*(df["perc_of_active_connections"]/100)) #correct for number of active connections
    df = df.loc[df["perc_of_active_connections"]!= 0] #remove inactive connections with energy consumption 
    
    return df

def InteractiveMap (data, filename, usage_col, caption_legend):
    """Creates a folium map (JS Leaflet) and saves it in the current working directory
    
    Parameters
    --------------
    data : dataframe 
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
    cmap = cm.LinearColormap(['green', 'yellow', 'red'], vmin=data[usage_col].min(), vmax=data[usage_col].max())
    cmap.caption = caption_legend
    
    # clean data
    interactive_map = folium.Map(location = [52.092876, 5.104480], zoom_start = 6.5)
    interactive_map.add_child(cmap)

    for i in range(len(data)):
        folium.CircleMarker(location = [data["LAT"].iloc[i], data["LON"].iloc[i]], 
                        radius = 2, weight = 0, fill_opacity = 1, fill = True, fill_color = cmap(data[usage_col].iloc[i])).add_to(interactive_map)

    interactive_map.save("{}.html".format(filename))
    
#%% DATA
data = pd.read_csv("data_energy_geo.csv")
os.chdir("../Results")

#%% PREPARATION FOR MAPS
start_year = data["year"].min()
last_year = data["year"].max() + 1

gas = {}
for i in range(start_year, last_year):
    gas["gas{}".format(i)] = MapData(data, "gas", i)

elec = {} 
for i in range(start_year, last_year):
    elec["elec{}".format(i)] = MapData(data, "electricity", i)

#%% MAPS [slow]
for i in gas:
    InteractiveMap(gas[i], "{}_cor".format(i), "annual_consume_corrected", "Gas consumption in {} (m3)".format(re.search(r"[0-9]{4}$", i).group()))
    print("finished {}".format(i))
   

for i in elec:
    InteractiveMap(elec[i], "{}_cor".format(i), "annual_consume_corrected", "Electricity consumption in {} (kWh)".format(re.search(r"[0-9]{4}$", i).group()))
    print("finished {}".format(i))

