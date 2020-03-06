# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 13:04:25 2020.

@author: laura
"""

import os
import re
import pandas as pd

# pylint: disable=C0103

def combineFiles(list_of_files):
    """Combine different csv files from the same working directory.

    Also corrects for shifted year labels.

    Parameters
    ----------
    list_of_files : list of csv files from working directory
    that have to be combined

    Returns
    -------
    data : pandas dataframe
        A single dataframe containing all data
    """
    data = []
    for file in list_of_files:
        df = pd.read_csv(file)
        name = file.replace(".csv", "")
        year = re.search(r"[0-9]{4}$", name).group()
        year_corrected = int(year) - 1  # correct for the year shift
        df["year"] = year_corrected
        data.append(df)

    data = pd.concat(data, sort=False)

    return data


def loadAndCombine(path, en_type):
    """Find all csv files in path and combine them to in dataframe.

    Uses combineFiles function.

    Parameters
    ----------
    path : str
        Path to data.
    en_type : str
        Energy type, used in the "type" column.

    Returns
    -------
    file_data : pandas dataframe
        A combination of all data of all the csv files
        in the directory given in path.
    """
    file_list = os.listdir(path)
    file_list = [path + i for i in file_list]  # add path to filenames
    file_data = combineFiles(file_list)
    file_data["type"] = en_type

    return file_data
