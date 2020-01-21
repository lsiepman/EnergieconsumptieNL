# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 13:19:54 2020

@author: laura
"""

# IMPORTS
import pandas as pd
import numpy as np
import re
import folium
import branca.colormap as cm
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import colorbar, colors
from matplotlib import cm as cmx
import cartopy.crs as ccrs

# FUNCTIONS
def CombineFiles(list_of_files):
    """ Combines different csv files from the same working directory. Corrects for shifted year labels.
        
    Parameters
    -----------
    list_of_files : list of csv files from working directory that have to be combined 
    
    Returns
    ----------
    dataframe
    """
    data = []
    for file in list_of_files:
        df = pd.read_csv(file)
        name = file.replace(".csv", "")
        year = re.search(r"[0-9]{4}$", name).group()
        year_corrected = int(year) - 1 #correct for the year shift
        df["year"] = year_corrected
        data.append(df)
        
    data = pd.concat(data, sort = False)    
         
    return data


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
    data = data.loc[data["perc_of_active_connections"]!= 0]
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
        
    data = data.loc[data["outlier"] == "no"]
    data = data.drop(["outlier"], axis = 1)
    
    return data


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
    cmap = cm.LinearColormap(['green', 'yellow', 'red'], vmin=data[usage_col].min(), vmax=data[usage_col].max())
    cmap.caption = caption_legend
    
    # clean data
    interactive_map = folium.Map(location = [52.092876, 5.104480], zoom_start = 6.5)
    interactive_map.add_child(cmap)

    for i in range(len(data)):
        folium.CircleMarker(location = [data["LAT"].iloc[i], data["LON"].iloc[i]], 
                        radius = 2, weight = 0, fill_opacity = 1, fill = True, fill_color = cmap(data[usage_col].iloc[i])).add_to(interactive_map)

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
    saves the html folium maps in the working directory
    """
    for i in energy_dict:
        PlotInteractiveMap(energy_dict[i], "{0}_{1}".format(filename_base, i), data_col, "{0} consumption in {1} ({2})".format(type_energy, re.search(r"[0-9]{4}$", i).group(), unit_energy)) 
        print("finished {}".format(i))
        
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