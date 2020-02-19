# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:42:49 2020.

@author: laura
"""
import os
import pandas as pd
from functions_interactive_map import MultipleInteractiveMaps


def main():
    # SETTINGS
    os.chdir("..")
    pd.set_option('max_columns', 25)

    DATA_PATH = os.getcwd() + "/Data/"
    RESULT_PATH = os.getcwd() + "/Results/Cities_Map_Interactive/"

    # DATA
    data = pd.read_csv(DATA_PATH + "data_energy_geo.csv")

    # PLOT PREP
    replacements = {"city": {"'S-GRAVENHAGE": "DENHAAG",
                             "'S GRAVENHAGE": "DENHAAG"}}
    data = data.replace(replacements)

    cities = ["AMSTERDAM", "ROTTERDAM", "DENHAAG", "UTRECHT",
              "EINDHOVEN", "GRONINGEN", "TILBURG", "ALMERE",
              "BREDA", "NIJMEGEN"]  # 10 largest cities

    # PLOT MAPS
    for city in cities:
        df = data.loc[data["city"] == city]
        gas = MultipleInteractiveMaps(df, "gas")
        elec = MultipleInteractiveMaps(df, "electricity")

        gas.plotMapYears(RESULT_PATH + "{0}_GAS".format(city), "m3")
        elec.plotMapYears(RESULT_PATH + "{0}_ELEC".format(city), "kWh")


if __name__ == "__main__":
    main()
