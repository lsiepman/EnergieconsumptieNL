# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 13:19:54 2020.

@author: laura
"""

import numpy as np


class GeneralFunctions:
    """Collection of functions used in multiple scripts."""

    @staticmethod
    def correctForConnection(data):
        """Correct energy usage for the number of active connections.

        Parameters
        ----------
        data : pandas dataframe
            contains the columns "annual_consume",
            "perc_of_active_connections", and
            "num_connections"

        Returns
        -------
        original dataframe with a new column for the corrected_annual_consume
        """
        data = data.loc[data["perc_of_active_connections"] != 0]

        orig_vals = data["annual_consume"]
        connects = data["num_connections"]
        perc_connects = data["perc_of_active_connections"]/100

        cor_connects = connects*perc_connects

        cor_vals = orig_vals/cor_connects

        data["annual_consume_corrected"] = cor_vals

        return data

    @staticmethod
    def removeOutliers(data, name_col):
        """Remove outliers from the data.

        Parameters
        ----------
        data : pandas dataframe
            the data containing possible outliers
        name_col : str
            name of the column to be analysed

        Returns
        -------
        dataframe without the outliers
        """
        data.reset_index(inplace=True, drop=True)
        threshold = 3
        mean_col = data[name_col].mean()
        std_col = data[name_col].std()
        data["not_outlier"] = True

        for i in range(len(data)):
            value = data[name_col][i]
            z_score = (value - mean_col)/std_col
            if np.abs(z_score) > threshold:
                data["not_outlier"][i] = False

        data = data.loc[data["not_outlier"]]
        data = data.drop(["not_outlier"], axis=1)

        return data
