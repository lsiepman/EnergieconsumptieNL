# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 12:46:34 2020

@author: laura
"""

#%% IMPORTS
from functions_cbs import CleanCBS
import os
import pandas as pd

#%% SETTINGS
os.chdir("../Data/CBS")
pd.set_option('max_columns', 25)

#%% DATA
lst_files = os.listdir()
lst_files = [i for i in lst_files if i.startswith("CBS") and "METADATA" not in i]

#%% DATA CLEANING
func = CleanCBS(lst_files)
files = func.ReadFiles()
files = func.StripCols()
files = func.CleanFiles()
files = func.CombineFiles()
files = func.SelectYears(2008, 2018)

#%% EXPORTING DATA
func.SaveCSV()
