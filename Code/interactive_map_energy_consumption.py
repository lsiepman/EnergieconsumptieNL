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

#%% SETTINGS
os.chdir("../Data")
pd.set_option('max_columns', 25)

#%% FUNCTIES
def DataJaarKaart(data, energiesoort, jaar):
    """Selecteert de data die in de kaart gebruikt zal worden.
    
    Parameters
    -----------
    data : dataframe met energieconsumptiedata
    energiesoort : str "gas", of "electricity"
    jaar : int jaar om te bekijken
    
    Returns
    -----------
    subset van oorspronkelijk dataframe
    """
    df = data.loc[(data["Soort"] == energiesoort) & (data["jaar"] == jaar)]
    df = df.dropna(subset = ["LAT", "LON"]).reset_index()
    
    return df

#def JaarKaart (data, filename, verbruik_kolom, caption_legend):
#    """Maakt een foliumkaart en slaat deze op in de huidige working directory
#    
#    Parameters
#    --------------
#    data : dataframe met subset van energieconsumptiedata
#    filename : str uiteindelijke bestandsnaam van de kaart, zonder bestandsextensie
#    verbruik_kolom : naam van de kolom waarin het verbruik staat
#    caption_legend
#
#    """
#    #color scale
#    cmap = cm.LinearColormap(['green', 'yellow', 'red'], vmin=data[verbruik_kolom].min(), vmax=data[verbruik_kolom].max())
#    cmap.caption = caption_legend
#    
#    # clean data
#    kaart = folium.Map(location = [52.092876, 5.104480], zoom_start = 8)
#    kaart.add_child(cmap)
#
#    for i in range(len(data)):
#        folium.CircleMarker(location = [data["LAT"].iloc[i], data["LON"].iloc[i]], 
#                        radius = 3, weight = 0, fill_opacity = 1, fill = True, fill_color = linear(gas2010["annual_consume"].iloc[i])).add_to(kaart)

    
    
#%% DATA
data = pd.read_csv("data_energie_geo.csv")

#%% VOORBEREIDING KAART
gas2010 = data.loc[(data["Soort"] == "gas") & (data["jaar"] == 2010)]

linear = cm.LinearColormap(['green', 'yellow', 'red'], vmin=3, vmax=10)

linear
#%% KAART
#kaart = folium.Map(location = [52.092876, 5.104480], zoom_start = 8)


#%% EXPORT
#os.chdir("../Results")
#kaart.save("Kaart.html")
