# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 10:22:48 2020.

Combining data
@author: laura
"""

import os
import pandas as pd
from functions_combine import loadAndCombine


def main():
    # SETTINGS
    os.chdir("..")
    GAS_PATH = os.getcwd() + "/Data/Gas/"
    ELECTRICITY_PATH = os.getcwd() + "/Data/Electricity/"
    pd.set_option('max_columns', 25)

    # DATA
    gas_data = loadAndCombine(GAS_PATH, "gas")
    elec_data = loadAndCombine(ELECTRICITY_PATH, "electricity")

    geo_info = pd.read_csv("Data/Geolocation.csv")

    # COMBINE DATA GAS AND ELECTRICITY
    data = pd.concat([gas_data, elec_data])

    geo_data = pd.merge(data, geo_info, left_on=["zipcode_from"],
                        right_on=["POSTCODE"],
                        how="left")

    # EXPORT
    geo_data.to_csv("Data/data_energy_geo.csv", index=False)


if __name__ == "__main__":
    main()
