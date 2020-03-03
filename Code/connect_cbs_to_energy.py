# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:06:02 2020.

@author: laura
"""

import os
import pandas as pd
import numpy as np
from functions_general import GeneralFunctions
from functions_cbs import ConnectEnergyCBS

# def main():
#    """Execute file."""
# SETTINGS
os.chdir("..")
CBS_PATH = os.getcwd() + "/Data/CBS/"
DATA_PATH = os.getcwd() + "/Data/"
pd.set_option("max_columns", 25)

# DATA
age = pd.read_csv(CBS_PATH + "Clean_CBS - Age (2008-2018).csv",
                  dtype={"ID": int, "Perioden": int, "Bevolking_1": float})
imm = pd.read_csv(CBS_PATH
                  + "Clean_CBS - Immigration (2008-2018).csv",
                  dtype={"ID": int, "Perioden": int, "Bevolking_1": float})
pos = pd.read_csv(CBS_PATH
                  + "Clean_CBS - Position_household (2008-2018).csv",
                  dtype={"ID": int, "Perioden": int, "Bevolking_1": float})
hou = pd.read_csv(CBS_PATH
                  + "Clean_CBS - Household_composition (2008-2018).csv")

energy = pd.read_csv(DATA_PATH + "data_energy_geo.csv")

# DATA PREPARATION ENERGY
gas = energy.loc[energy["type"] == "gas"]
elec = energy.loc[energy["type"] == "electricity"]
del energy

gas = GeneralFunctions.correctForConnection(gas)
gas.drop(["net_manager", "purchase_area", "street",
          "zipcode_from", "zipcode_to", "city",
          "type_conn_perc", "type_of_connection",
          "LON", "LAT"], axis=1, inplace=True)
gas = GeneralFunctions.removeOutliers(gas, "annual_consume_corrected")
gas["Postcode4"] = gas["POSTCODE"].str.extract("([0-9]+)")

gas_mean = gas.groupby(["Postcode4", "year"]).mean()
gas_median = gas.groupby(["Postcode4", "year"]).median()

# DATA PREPARATION CBS
c = ConnectEnergyCBS()
c.splitYears(age, "Perioden")
age_years = c.returnDataDict()
orig = age_years[2008]
orig = orig.loc[orig["Leeftijd"] != "Total"]
# make age a ordinal variable:
age_list = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30',
            '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '60-65',
            '65-70', '70-75', '75-80', '80-85', '85-90', '90-95', '95<']
age_dict = dict(zip(age_list, np.arange(len(age_list))))

orig["Age_score"] = orig["Leeftijd"].map(age_dict)

test = age_years[2008].pivot_table(index=["Postcode"],
                                   columns=["Geslacht", "Leeftijd"],
                                   values="Bevolking_1")

test2 = orig.pivot_table(index=["Postcode"],
                         columns=["Geslacht", "Age_score"],
                         values="Bevolking_1")

# if __name__ == "__main__":
#     main()
