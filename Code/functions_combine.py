# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 13:04:25 2020

@author: laura
"""
#%% IMPORTS
import pandas as pd
import re

#%% FUNCTIONS
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
