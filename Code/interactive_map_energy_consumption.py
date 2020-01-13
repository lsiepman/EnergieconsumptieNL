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
import numpy as np
from tqdm import tqdm

#%% SETTINGS
os.chdir("../Data")
pd.set_option('max_columns', 25)

#%% FUNCTIONS
def CorrectForConnection(data):
    """Corrects energy usage for the number of active connections
    
    Parameters
    -----------
    data : pandas dataframe
        contains the columns "annual_consume", "perc_of_active_connections", and "num_connections"
        
    Returns
    ---------
    original dataframe with a new column for the corrected_annual_consume
    """
    data["annual_consume_corrected"] = data["annual_consume"]/(data["num_connections"]*(data["perc_of_active_connections"]/100))
    
    return data


def MapData(data, energy_type, year):
    """Selects the data for the map. Removes rows with 0 active connections and corrects for the number of active connections per zipcode.
    
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

def InteractiveMap (data, filename, usage_col, caption_legend):
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
    cmap = cm.LinearColormap(['green', 'yellow', 'red'], vmin=data[usage_col].min(), vmax=data[usage_col].max())
    cmap.caption = caption_legend
    
    # clean data
    interactive_map = folium.Map(location = [52.092876, 5.104480], zoom_start = 6.5)
    interactive_map.add_child(cmap)

    for i in range(len(data)):
        folium.CircleMarker(location = [data["LAT"].iloc[i], data["LON"].iloc[i]], 
                        radius = 2, weight = 0, fill_opacity = 1, fill = True, fill_color = cmap(data[usage_col].iloc[i])).add_to(interactive_map)

    interactive_map.save("{}.html".format(filename))


def RemoveOutliers(data, name_col):
    """Removes outliers from the data
    
    Parameters
    ------------
    data : pandas dataframe
        the data containing possible outliers
    name_col : str
        name of the column to be analysed
        
    Returns
    ------------
    dataframe without the outliers
    """

    data.reset_index(inplace = True, drop = True)
    threshold = 3
    mean_col = data[name_col].mean()
    std_col = data[name_col].std()
    data["outlier"] = "no"
    
    for i in tqdm(range(len(data))):
        j = data[name_col][i]
        z = (j - mean_col)/std_col
        if np.abs(z) > threshold:
            data["outlier"][i] = "yes"
        
    data = data.loc[data["outlier"] != "yes"]
    data.drop(["outlier"], inplace = True)
    
    return data
#%% DATA
data = pd.read_csv("data_energy_geo.csv")
os.chdir("../Results")

#%% PREPARATION FOR MAPS
start_year = data["year"].min()
last_year = data["year"].max() + 1

gas = {}
for i in range(start_year, last_year):
    gas["gas{}".format(i)] = MapData(data, "gas", i)
    gas["gas{}".format(i)] = RemoveOutliers(gas["gas{}".format(i)], "annual_consume_corrected")

elec = {} 
for i in range(start_year, last_year):
    elec["elec{}".format(i)] = MapData(data, "electricity", i)
    elec["elec{}".format(i)] = RemoveOutliers(elec["elec{}".format(i)], "annual_consume_corrected")

#%% MAPS [slow]
for i in gas:
    InteractiveMap(gas[i], "{}_cor".format(i), "annual_consume_corrected", "Gas consumption in {} (m3)".format(re.search(r"[0-9]{4}$", i).group()))
    print("finished {}".format(i))
   

for i in elec:
    InteractiveMap(elec[i], "{}_cor".format(i), "annual_consume_corrected", "Electricity consumption in {} (kWh)".format(re.search(r"[0-9]{4}$", i).group()))
    print("finished {}".format(i))

#%% REMOVING HIGH CONSUMPTION TEST
#for i in gas:
#    print(i)
#    print("mean:", gas[i]["annual_consume_corrected"].mean())
#    print("median:", gas[i]["annual_consume_corrected"].median())
#    print("std:", gas[i]["annual_consume_corrected"].std())
#    print("min", gas[i]["annual_consume_corrected"].min())
#    print("max", gas[i]["annual_consume_corrected"].max()) 
#    print("\n")       
#    
#gas_test = RemoveOutliers(gas["gas2010"], "annual_consume_corrected")
#gas_test = gas_test.loc[gas_test["outlier"] != "yes"]
#InteractiveMap(gas_test, "test_outlier_removal", "annual_consume_corrected", "Gas consumption in 2010 (m3)")
