# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 10:25:42 2020.

@author: laura
"""

import os
import pandas as pd
import numpy as np
from functions_general import GeneralFunctions as GF
from functions_cbs import ConnectEnergyCBS as CEC

# def main():
#    """Execute file."""
# SETTINGS
os.chdir("..")
DATA_PATH = os.getcwd() + "/Data/"
RESULTS_PATH = os.getcwd() + "/Results/"
pd.set_option("max_columns", 25)
pd.options.mode.chained_assignment = None

# DATA
energy = pd.read_csv(DATA_PATH + "data_energy_geo.csv")

# DATA PREP
en_cols_to_drop = ["net_manager", "purchase_area", "street", "zipcode_from",
                   "zipcode_to", "city", "type_conn_perc",
                   "type_of_connection", "LON", "LAT"]

energy.drop(en_cols_to_drop, axis=1, inplace=True)
energy = GF.correctForConnection(energy)

gas_mean, gas_median = CEC.groupEnergy(energy, "gas")
elec_mean, elec_median = CEC.groupEnergy(energy, "electricity")
del energy

energy_mean = gas_mean.merge(elec_mean, left_index=True, right_index=True,
                             suffixes=("_GAS", "_ELEC"))
energy_median = gas_median.merge(elec_median, left_index=True,
                                 right_index=True,
                                 suffixes=("_GAS", "_ELEC"))

# CALC DISTANCES
gas_mean_cec = CEC()
gas_mean_cec.splitGroup(gas_mean, "year")
gas_mean_cec.calcDistances()
gmcec = gas_mean_cec.returnDict("distance")


test = gmcec[2010]
test2 = pd.DataFrame(test.unstack())
test2.index.names = ["PostcodeA", "PostcodeB"]
test2.columns = ["Distance"]
test2.reset_index(inplace=True)
test2 = test2.loc[pd.DataFrame(
                  np.sort(test2[['PostcodeA', 'PostcodeB']], 1),
                  index=test2.index).drop_duplicates(keep='first').index]
test2.replace(0, np.nan, inplace=True)
test3 = test2.nsmallest(50, "Distance")
